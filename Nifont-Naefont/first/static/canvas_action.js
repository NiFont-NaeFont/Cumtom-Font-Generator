var canvas, context, tool;

var cnt = 2;

var array_uni = [];
array_uni = ['AC00', 'AC1D', 'AC3A', 'AC57', 'AC74', 'AC91', 'ACAE', 'ACCB', 'ACE8', 'AD05', 'AD22', 'AD3F', 'AD5C', 'AD79', 'AD96', 'ADB3', 'ADD0', 'ADED', 'AE0A', 'AE27', 'AE44', 'AE61', 'AE7E', 'AE9B',
         'AEB8', 'AED5', 'AEF2', 'AF0F', 'AF10', 'AF2D', 'AF4A', 'AF67', 'AF84', 'AFA1', 'AFBE', 'AFDB', 'AFF8', 'B015', 'B032', 'B04F', 'B06C', 'B089', 'B0A6', 'B0C3', 'B0E0', 'B0FD', 'B11A', 'B137', 'B154', 'B171', 
         'B18E', 'B1AB', 'B1C8', 'B1E5', 'B202', 'B21F', 'B220', 'B23D', 'B25A', 'B277', 'B294', 'B2B1', 'B2CE', 'B2EB', 'B308', 'B325', 'B342', 'B35F', 'B37C', 'B399', 'B3B6', 'B3D3', 'B3F0', 'B40D', 'B42A', 'B447',
         'B464', 'B481', 'B49E', 'B4BB', 'B4D8', 'B4F5', 'B512', 'B52F', 'B530', 'B54D', 'B56A', 'B587', 'B5A4', 'B5C1', 'B5DE', 'B5FB', 'B618', 'B635', 'B652', 'B66F', 'B68C', 'B6A9', 'B6C6', 'B6E3', 'B700', 'B71D',
         'B73A', 'B757', 'B774', 'B791', 'B7AE', 'B7CB', 'B7E8', 'B805', 'B822', 'B83F', 'B840', 'B85D', 'B87A', 'B897', 'B8B4', 'B8D1', 'B8EE', 'B90B', 'B928', 'B945', 'B962', 'B97F', 'B99C', 'B9B9', 'B9D6', 'B9F3',
         'BA10', 'BA2D', 'BA4A', 'BA67', 'BA84', 'BAA1', 'BABE', 'BADB', 'BAF8', 'BB15', 'BB32', 'BB4F', 'BB50', 'BB6D', 'BB8A', 'BBA7', 'BBC4', 'BBE1', 'BBFE', 'BC1B', 'BC38', 'BC55', 'BC72', 'BC8F', 'BCAC', 'BCC9',
         'BCE6', 'BD03', 'BD20', 'BD3D', 'BD5A', 'BD77', 'BD94', 'BDB1', 'BDCE', 'BDEB', 'BE08', 'BE25', 'BE42', 'BE5F', 'BE60', 'BE7D', 'BE9A', 'BEB7', 'BED4', 'BEF1', 'BF0E', 'BF2B', 'BF48', 'BF65', 'BF82', 'BF9F', 
         'BFBC', 'BFD9', 'BFF6', 'C013', 'C030', 'C04D', 'C06A', 'C087', 'C0A4', 'C0C1', 'C0DE', 'C0FB', 'C118', 'C135', 'C152', 'C16F', 'C170', 'C18D', 'C1AA', 'C1C7', 'C1E4', 'C201', 'C21E', 'C23B', 'C258', 'C275', 
         'C292', 'C2AF', 'C2CC', 'C2E9', 'C306', 'C323', 'C340', 'C35D', 'C37A', 'C397', 'C3B4', 'C3D1', 'C3EE', 'C40B', 'C428', 'C445', 'C462', 'C47F', 'C480', 'C49D', 'C4BA', 'C4D7', 'C4F4', 'C511', 'C52E', 'C54B', 
         'C568', 'C585', 'C5A2', 'C5BF', 'C5DC', 'C5F9', 'C616', 'C633', 'C650', 'C66D', 'C68A', 'C6A7', 'C6C4', 'C6E1', 'C6FE', 'C71B', 'C738', 'C755', 'C772', 'C78F', 'C790', 'C7AD', 'C7CA', 'C7E7', 'C804', 'C821', 
         'C83E', 'C85B', 'C878', 'C895', 'C8B2', 'C8CF', 'C8EC', 'C909', 'C926', 'C943', 'C960', 'C97D', 'C99A', 'C9B7', 'C9D4', 'C9F1', 'CA0E', 'CA2B', 'CA48', 'CA65', 'CA82', 'CA9F', 'CAA0', 'CABD', 'CADA', 'CAF7', 
         'CB14', 'CB31', 'CB4E', 'CB6B', 'CB88', 'CBA5', 'CBC2', 'CBDF', 'CBFC', 'CC19', 'CC36', 'CC53', 'CC70', 'CC8D', 'CCAA', 'CCC7', 'CCE4', 'CD01', 'CD1E', 'CD3B', 'CD58', 'CD75', 'CD92', 'CDAF', 'CDB0', 'CDCD', 
         'CDEA', 'CE07', 'CE24', 'CE41', 'CE5E', 'CE7B', 'CE98', 'CEB5', 'CED2', 'CEEF', 'CF0C', 'CF29', 'CF46', 'CF63', 'CF80', 'CF9D', 'CFBA', 'CFD7', 'CFF4', 'D011', 'D02E', 'D04B', 'D068', 'D085', 'D0A2', 'D0BF', 
         'D0C0', 'D0DD', 'D0FA', 'D117', 'D134', 'D151', 'D16E', 'D18B', 'D1A8', 'D1C5', 'D1E2', 'D1FF', 'D21C', 'D239', 'D256', 'D273', 'D290', 'D2AD', 'D2CA', 'D2E7', 'D304', 'D321', 'D33E', 'D35B', 'D378', 'D395', 
         'D3B2', 'D3CF', 'D3D0', 'D3ED', 'D40A', 'D427', 'D444', 'D461', 'D47E', 'D49B', 'D4B8', 'D4D5', 'D4F2', 'D50F', 'D52C', 'D549', 'D566', 'D583', 'D5A0', 'D5BD', 'D5DA', 'D5F7', 'D614', 'D631', 'D64E', 'D66B', 
         'D688', 'D6A5', 'D6C2', 'D6DF', 'D6E0', 'D6FD', 'D71A', 'D737', 'D754', 'D771', 'D78E'];

// window.onload를 통해 시작시에 function()실행
window.onload = function(){

  // getElementById메서드로 canvas요소를 표시할 DOM을 호출
  canvas = document.getElementById('drawCanvas');

  // canvas그리기를 수행하기 위해 getContext()메서드를 호출
  context = canvas.getContext('2d');
  context.lineWidth = 5;// 선굵기 초기 설정

  // 마우스 움직임에 따른 그리기 이벤트 등록
  tool = new tool_pencil();
  canvas.addEventListener('mousedown', ev_canvas, false);
  canvas.addEventListener('mousemove', ev_canvas, false);
  canvas.addEventListener('mouseup',   ev_canvas, false);
}

// 그림판에 그린 그림 저장
function saveBoard(cnt)
   {
      var link = document.createElement('a');
      // //link.href = "C:/Users/82108/Desktop/중앙대학교/취준/해커톤/대웅/DaeWoong/Goodrug/first/static/Font";


      link.download = "uni"+ array_uni[cnt] +".png";
      link.href = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
      link.click();
   }

// 그림판 그림 지우기
function clearBoard()
   {
     context.clearRect(0, 0, canvas.width, canvas.height);
     context.beginPath();
     document.getElementById('show').innerText = "Blank";
   }

// 그림판 선굵기 변경
//function changeLineWidth(width)
//   {
//     context.lineWidth = width;
//   }

// 그리기 펜 움직임 설정
function tool_pencil ()
{
    var tool = this;

    this.started = false;
    this.mousedown = function (ev)
    {
        context.beginPath();
        context.moveTo(ev._x, ev._y);
        tool.started = true;
    };

    this.mousemove = function (ev)
    {
        if (tool.started)
        {
            context.lineTo(ev._x, ev._y);
            context.stroke();
        }
    };

    this.mouseup = function (ev)
    {
      if (tool.started){
            tool.mousemove(ev);
            tool.started = false;
      }
    };

    this.mousedown = function (ev)
    {
        context.beginPath();
        context.moveTo(ev._x, ev._y);
        tool.started = true;
    };

    this.mousemove = function (ev)
    {
        if (tool.started)
        {
            context.lineTo(ev._x, ev._y);
            context.stroke();
        }
    };

    this.mouseup = function (ev)
    {
      if (tool.started){
            tool.mousemove(ev);
            tool.started = false;
      }
    };
}

function ev_canvas (ev)
{
    if (ev.layerX || ev.layerX == 0)
    {
      ev._x = ev.layerX;
      ev._y = ev.layerY;
    }
    else if (ev.offsetX || ev.offsetX == 0)
    {
      ev._x = ev.offsetX;
      ev._y = ev.offsetY;
    }
    var func = tool[ev.type];
    if (func) {
        func(ev);
    }
}
