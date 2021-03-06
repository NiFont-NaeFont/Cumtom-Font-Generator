const svg2ttf = require("svg2ttf");
const ImageTracer = require("./imagetracer_v1.2.1");
const PNG = require("pngjs").PNG;
const fs = require("graceful-fs"); // EMFILE 에러 해결을 위한 fs 라이브러리
const SVGIcons2SVGFontStream = require("svgicons2svgfont");

//const save_dir = "./save_dir";
const save_dir = process.argv[2]; // 실행 인자 받기. node generate_ttf.js ./save_dir

console.log("\nStart converting into ttf...\n");

let fontStream = new SVGIcons2SVGFontStream({
  fontName: "customFont",
});

// 폴더 에러 방지
try {
  fs.statSync("svg_font");
} catch (err) {
  if (err.code === "ENOENT") {
    fs.mkdirSync("svg_font");
  }
}

try {
  fs.statSync("svgs");
} catch (err) {
  if (err.code === "ENOENT") {
    fs.mkdirSync("svgs");
  }
}

try {
  fs.statSync("fonts");
} catch (err) {
  if (err.code === "ENOENT") {
    fs.mkdirSync("fonts");
  }
}

let fileNames = fs.readdirSync(save_dir);

let sources = [];

// 원본 파일 이름으로부터 유니코드명 및 svg 파일 이름 추출
for (let i = 0; i < fileNames.length; i++) {
  sources[i] = "0x" + fileNames[i].substring(9,).substring(0, 4);
  //console.log("소스파일 : "+ sources[i]);
}

// 각각의 이미지로부터 각각의 SVG 파일 생성
for (let i = 0; i < fileNames.length; i++) {
  //console.log("iiiii :  "+i)
  let j = i;
  //console.log("데이터  :  "+fileNames[j].substring(9,))
  let data = fs.readFileSync(`${save_dir}/${fileNames[j]}`);
  
  //console.log("각각으로부터 svg 생성"+data)
  let png = PNG.sync.read(data);

  let imageData = {
    width: png.width,
    height: png.height,
    data: png.data,
  };

  // 벡터화 옵션 (폰트 스타일)
  // 왠진 모르겠는데 옵션이 안 먹힘
  let options = {
    ltres: 1.0,
    qtres: 1.0,
    strokewidth: 1.0,
    pathomit: 1.0,
    blurradius: 1.0,
    blurdelta: 1.0,
  };
  options.pal = [
    { r: 0, g: 0, b: 0, a: 255 },
    { r: 255, g: 255, b: 255, a: 255 },
  ];
  options.linefilter = true;

  let svgString = ImageTracer.imagedataToSVG(imageData, options);
  fs.writeFileSync(`svgs/${fileNames[j].substring(9,).replace(".png", "")}.svg`, svgString);

  console.log(`Made : svgs/${fileNames[j].substring(9,).replace(".png", "")}.svg`);
}

// 폰트 이벤트리스너
fontStream
  .pipe(fs.createWriteStream("svg_font/font.svg"))
  .on("finish", () => {
    let svgdata = fs.readFileSync("svg_font/font.svg", "utf8");

    console.log("Changing svg into ttf...");
    let ttf = svg2ttf(svgdata, {});

    console.log("Writing ttf data into .ttf file...");
    fs.writeFileSync("fonts/customfont.ttf", Buffer.from(ttf.buffer));
  })
  .on("error", (err) => {
    console.log(err);
  });

// 여러 SVG 파일들을 하나의 SVG 파일로 생성
for (let i = 0; i < sources.length; i++) {
  let glyph = fs.createReadStream(
    `svgs/${fileNames[i].substring(9,13).replace(".png", "")}.svg`
  );
  glyph.metadata = {
    unicode: [String.fromCharCode(sources[i].toString(10))],
    name: `glyph${sources[i]}`,
  };
  console.log(`Writing into svg_font.svg -> ${String.fromCharCode(sources[i].toString(10))}`);
  fontStream.write(glyph);
}

fontStream.end();

console.log("\nDone converting into ttf!\n");
