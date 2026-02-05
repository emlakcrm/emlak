// tools/update-heads.js
// Node script: tüm .html dosyalarını tarar, AdSense kodlarını kaldırır,
// head-template.html ile head değiştirir ve aos-init.html'i body sonuna ekler.
// NOT: Önce preview olarak "<file>.updated" üretir. Orijinalleri otomatik overwrite etmez.

const fs = require('fs');
const path = require('path');
const glob = require('glob');

const TEMPLATE_PATH = path.join(__dirname, 'head-template.html');
const AOS_INIT_PATH = path.join(__dirname, 'aos-init.html');
const SITE_BASE = 'https://www.selmangunes.com.tr'; // canonical temel domain

if (!fs.existsSync(TEMPLATE_PATH)) {
  console.error('head-template.html bulunamadı:', TEMPLATE_PATH);
  process.exit(1);
}
if (!fs.existsSync(AOS_INIT_PATH)) {
  console.error('aos-init.html bulunamadı:', AOS_INIT_PATH);
  process.exit(1);
}

const headTemplate = fs.readFileSync(TEMPLATE_PATH, 'utf8');
const aosInit = fs.readFileSync(AOS_INIT_PATH, 'utf8');

function computeCanonical(filePath) {
  const rel = path.relative(process.cwd(), filePath).replace(/\\/g, '/');
  if (rel.endsWith('index.html')) {
    const dir = path.dirname(rel);
    return dir === '.' ? SITE_BASE + '/' : SITE_BASE + '/' + dir + '/';
  }
  return SITE_BASE + '/' + rel;
}

function extractTitle(html) {
  const m = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  return m ? m[1].trim() : '';
}
function extractDescription(html) {
  const m = html.match(/<meta\s+name=["']description["']\s+content=["']([\s\S]*?)["']/i);
  return m ? m[1].trim() : '';
}
function removeAdsense(html) {
  // Remove AdSense external script lines and ins.adsbygoogle blocks and inline pushes
  html = html.replace(/<script[^>]*pagead2\.googlesyndication\.com[^>]*>[\s\S]*?<\/script>/gi, '');
  html = html.replace(/<script[^>]*adsbygoogle[^>]*>[\s\S]*?<\/script>/gi, '');
  html = html.replace(/<ins[^>]*class=["']adsbygoogle["'][\s\S]*?<\/ins>/gi, '');
  return html;
}

glob("**/*.html", { ignore: ["node_modules/**", "tools/**", ".git/**"] }, (err, files) => {
  if (err) { console.error(err); process.exit(1); }
  files.forEach(file => {
    try {
      let html = fs.readFileSync(file, 'utf8');

      // 1) remove AdSense
      html = removeAdsense(html);

      // 2) extract title/description
      const title = extractTitle(html) || 'Selman Güneş Gayrimenkul';
      const desc = extractDescription(html) || `Sayfa: ${title} - Selman Güneş Gayrimenkul`;

      // 3) build canonical
      const canonical = computeCanonical(file);

      // 4) create head from template
      let newHead = headTemplate.replace(/{{TITLE}}/g, title)
                                .replace(/{{DESCRIPTION}}/g, desc)
                                .replace(/{{CANONICAL}}/g, canonical)
                                .replace(/{{OG_IMAGE}}/g, `${SITE_BASE}/img/logo.png`);

      // 5) replace existing head block if present
      if (/<head[\s\S]*?>[\s\S]*?<\/head>/i.test(html)) {
        html = html.replace(/<head[\s\S]*?>[\s\S]*?<\/head>/i, newHead);
      } else {
        // no head -> insert at top
        html = newHead + '\n' + html;
      }

      // 6) ensure aos-init exists before </body>
      if (!/AOS\.init\(/i.test(html)) {
        if (html.match(/<\/body>/i)) {
          html = html.replace(/<\/body>/i, aosInit + '\n</body>');
        } else {
          html = html + '\n' + aosInit;
        }
      }

      // 7) write preview file
      const outPath = file + '.updated';
      fs.writeFileSync(outPath, html, 'utf8');
      console.log('Preview created:', outPath);
    } catch (e) {
      console.error('Error processing', file, e);
    }
  });
  console.log('Tamamlandı. .updated dosyalarını kontrol edin, sonra isterseniz orijinallerle değiştirin.');
});
