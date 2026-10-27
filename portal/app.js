const base = document.body.dataset.base || './';
const normalise = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('en-GB');

document.addEventListener('keydown', event => {
  if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) {
    event.preventDefault();
    document.querySelector('#global-search').focus();
  }
});

const atlas = document.querySelector('#atlas-filters');
if (atlas) {
  const grid = document.querySelector('#atlas-grid');
  const cards = [...grid.querySelectorAll('.taxon-tile')];
  const fields = ['q', 'group', 'kind', 'period', 'sort'];
  const params = new URLSearchParams(location.search);
  for (const field of fields) if (params.has(field)) atlas.elements[field].value = params.get(field);
  function filterAtlas(updateURL = true) {
    const values = Object.fromEntries(new FormData(atlas));
    const terms = normalise(values.q.trim()).split(/\s+/).filter(Boolean);
    let count = 0;
    cards.sort((a, b) => values.sort === 'age'
      ? Number(b.dataset.age) - Number(a.dataset.age) || a.dataset.name.localeCompare(b.dataset.name)
      : a.dataset.name.localeCompare(b.dataset.name));
    for (const card of cards) {
      const data = card.dataset;
      const visible = terms.every(term => normalise(data.search).includes(term))
        && (!values.group || values.group === data.group)
        && (!values.kind || values.kind === data.kind)
        && (!values.period || (values.period === 'extant' ? data.kind === 'extant' : data.periods.split(' ').includes(values.period)));
      card.hidden = !visible;
      if (visible) count++;
      grid.append(card);
    }
    document.querySelector('#atlas-count').textContent = `${count} of ${cards.length} cards`;
    document.querySelector('#atlas-empty').hidden = count > 0;
    if (updateURL) {
      const next = new URLSearchParams();
      for (const field of fields) if (values[field] && !(field === 'sort' && values[field] === 'name')) next.set(field, values[field]);
      history.replaceState(null, '', `${location.pathname}${next.size ? '?' + next : ''}`);
    }
  }
  atlas.addEventListener('input', () => filterAtlas());
  atlas.addEventListener('submit', event => { event.preventDefault(); filterAtlas(); });
  atlas.addEventListener('reset', () => setTimeout(filterAtlas, 0));
  document.querySelector('[data-reset-atlas]').addEventListener('click', () => atlas.reset());
  window.addEventListener('popstate', () => {
    const current = new URLSearchParams(location.search);
    for (const field of fields) atlas.elements[field].value = current.get(field) || (field === 'sort' ? 'name' : '');
    filterAtlas(false);
  });
  filterAtlas(false);
}

const searchForm = document.querySelector('#library-search');
if (searchForm) {
  const query = document.querySelector('#search-query');
  const results = document.querySelector('#search-results');
  const count = document.querySelector('#search-count');
  const params = new URLSearchParams(location.search);
  let index;
  let request = 0;
  query.value = params.get('q') || '';
  document.querySelector('#global-search').value = query.value;

  function excerpt(text, terms) {
    const normal = normalise(text);
    const position = Math.min(...terms.map(term => normal.indexOf(term)).filter(position => position >= 0));
    const start = Number.isFinite(position) ? Math.max(0, position - 95) : 0;
    return (start ? '…' : '') + text.slice(start, start + 300) + (text.length > start + 300 ? '…' : '');
  }

  function highlighted(text, terms) {
    const fragment = document.createDocumentFragment();
    const normal = normalise(text);
    let cursor = 0;
    while (cursor < text.length) {
      const matches = terms.map(term => ({ at: normal.indexOf(term, cursor), length: term.length })).filter(match => match.at >= 0).sort((a, b) => a.at - b.at);
      if (!matches.length) { fragment.append(document.createTextNode(text.slice(cursor))); break; }
      const match = matches[0];
      fragment.append(document.createTextNode(text.slice(cursor, match.at)));
      const mark = document.createElement('mark');
      mark.textContent = text.slice(match.at, match.at + match.length);
      fragment.append(mark);
      cursor = match.at + match.length;
    }
    return fragment;
  }

  async function search(updateURL = true) {
    const thisRequest = ++request;
    const value = query.value.trim();
    const terms = normalise(value).split(/\s+/).filter(Boolean);
    results.replaceChildren();
    if (updateURL) history.replaceState(null, '', `${location.pathname}${value ? '?q=' + encodeURIComponent(value) : ''}`);
    if (!terms.length) { count.textContent = 'Enter a word or phrase to search.'; return; }
    count.textContent = 'Searching the collection…';
    try {
      if (!index) {
        const response = await fetch(base + 'search-index.json');
        if (!response.ok) throw new Error('Search index unavailable');
        index = await response.json();
      }
      if (thisRequest !== request) return;
      const matches = index.map(entry => {
        const title = normalise(entry.title);
        const text = normalise(entry.text);
        const match = terms.every(term => title.includes(term) || text.includes(term));
        const score = terms.reduce((sum, term) => sum + (title.includes(term) ? 20 : 0) + (text.includes(term) ? 1 : 0), 0);
        return { ...entry, match, score };
      }).filter(entry => entry.match).sort((a, b) => b.score - a.score || a.title.localeCompare(b.title));
      count.textContent = `${matches.length} ${matches.length === 1 ? 'result' : 'results'} for “${value}”`;
      if (!matches.length) {
        const message = document.createElement('p');
        message.textContent = 'No matching documents or cards. Try a shorter term or a different spelling.';
        results.append(message);
      }
      for (const entry of matches) {
        const article = document.createElement('article');
        article.className = 'search-result';
        const type = document.createElement('p');
        type.className = 'eyebrow';
        type.textContent = entry.type;
        const heading = document.createElement('h2');
        const link = document.createElement('a');
        link.href = base + entry.url;
        link.append(highlighted(entry.title, terms));
        heading.append(link);
        const snippet = document.createElement('p');
        snippet.append(highlighted(excerpt(entry.text, terms), terms));
        article.append(type, heading, snippet);
        results.append(article);
      }
    } catch {
      if (thisRequest !== request) return;
      count.textContent = 'Search could not load. Please reload, or browse the reading room and atlas.';
    }
  }
  searchForm.addEventListener('submit', event => { event.preventDefault(); search(); });
  let timer;
  query.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(search, 160); });
  window.addEventListener('popstate', () => { query.value = new URLSearchParams(location.search).get('q') || ''; search(false); });
  search(false);
}
