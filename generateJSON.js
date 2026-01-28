const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const sources = [
  { dir: './ilanlar', type: 'ilan', priority: 3 },
  { dir: './blog', type: 'blog', priority: 2 },
  { dir: './bilgi', type: 'bilgi', priority: 1 }
];

const outputFile = './data/search-index.json';
let allData = [];

sources.forEach(({ dir, type, priority }) => {
  if (!fs.existsSync(dir)) return;
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

  files.forEach(file => {
    const filePath = path.join(dir, file);
    const html = fs.readFileSync(filePath, 'utf-8');
    const $ = cheerio.load(html);

    const title = $('title').text() || $('h1').first().text() || file;
    const tagsAttr = $('meta[name="keywords"]').attr('content') || '';
    const tags = tagsAttr.split(',').map(t=>t.trim()).filter(t=>t);
    const img = $('img').first().attr('src') || '';

    allData.push({
      type,
      priority,
      title,
      tags,
      url: '/' + path.relative('.', filePath).replace(/\\/g,'/'),
      img
    });
  });
});

fs.writeFileSync(outputFile, JSON.stringify(allData, null, 2));
console.log(`${outputFile} oluşturuldu. Toplam: ${allData.length} içerik.`);
