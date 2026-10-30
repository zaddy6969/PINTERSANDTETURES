export default async function handler(request) {
  const sourceUrl = 'https://raw.githubusercontent.com/zaddy6969/PINTERSANDTETURES/main/index.html';
  const response = await fetch(sourceUrl, { cache: 'no-store' });

  if (!response.ok) {
    return new Response('Unable to load site', { status: 502 });
  }

  let html = await response.text();
  const stylesheet = '<link rel="stylesheet" href="/footer-fix.css?v=5">';

  if (!html.includes('href="/footer-fix.css')) {
    html = html.replace('</head>', `${stylesheet}\n</head>`);
  }

  return new Response(html, {
    status: 200,
    headers: {
      'content-type': 'text/html; charset=utf-8',
      'cache-control': 'public, s-maxage=60, stale-while-revalidate=86400'
    }
  });
}
