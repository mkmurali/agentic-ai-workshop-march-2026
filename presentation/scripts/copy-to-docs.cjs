const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const outDir = path.resolve(root, '..', 'docs', 'presentation');

const files = [
  ['index.html', 'index.html'],
  ['css/custom.css', 'css/custom.css'],
  ['images/agenticpi-day.png', 'images/agenticpi-day.png'],
];

fs.mkdirSync(path.join(outDir, 'css'), { recursive: true });
fs.mkdirSync(path.join(outDir, 'images'), { recursive: true });
for (const [src, dest] of files) {
  const srcPath = path.join(root, src);
  const destPath = path.join(outDir, dest);
  if (fs.existsSync(srcPath)) {
    fs.copyFileSync(srcPath, destPath);
    console.log('Copied', dest, '->', outDir);
  }
}
console.log('Presentation copied to docs/presentation (CSS paths are relative).');
