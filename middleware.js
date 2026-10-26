export default async function middleware(request) {
  const response = await fetch(request);
  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('text/html')) return response;

  let html = await response.text();
  const seo = `
<meta name="description" content="Painters & Textures provides professional painting, wall texture, decorative finish, interior and exterior painting services. Quality Finishes. Lasting Impressions.">
<meta name="keywords" content="painters and textures, painting services, wall texture, texture painting, interior painting, exterior painting, decorative wall finishes, residential painting, commercial painting">
<meta name="author" content="Painters & Textures">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="canonical" href="https://paintersandtextures.com/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#292a24">
<meta property="og:type" content="website">
<meta property="og:url" content="https://paintersandtextures.com/">
<meta property="og:title" content="Painters & Textures | Quality Finishes. Lasting Impressions.">
<meta property="og:description" content="Professional painting, wall texture and decorative finish work. Quality Finishes. Lasting Impressions.">
<meta property="og:site_name" content="Painters & Textures">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Painters & Textures | Quality Finishes. Lasting Impressions.">
<meta name="twitter:description" content="Professional painting and texture work with quality finishes and lasting impressions.">
<script type="application/ld+json">${JSON.stringify({
  '@context':'https://schema.org',
  '@type':'LocalBusiness',
  '@id':'https://paintersandtextures.com/#business',
  name:'Painters & Textures',
  url:'https://paintersandtextures.com/',
  telephone:'+917026193396',
  email:'paintersandtextures@gmail.com',
  slogan:'Quality Finishes. Lasting Impressions.',
  description:'Professional painting and texture work with quality finishes and lasting impressions.',
  areaServed:'India',
  serviceType:['Interior painting','Exterior painting','Wall texture work','Decorative finishes','Residential painting','Commercial painting']
})}</script>`;

  if (!html.includes('https://paintersandtextures.com/#business')) {
    html = html.replace('</head>', `${seo}\n</head>`);
  }

  return new Response(html, {
    status: response.status,
    headers: response.headers,
  });
}

export const config = { matcher: ['/((?!robots\\.txt|sitemap\\.xml|site\\.webmanifest|favicon\\.svg).*)'] };
