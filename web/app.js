'use strict';
const {move,spawn,canMove}=Game2048;
const $=selector=>document.querySelector(selector);
let board,score,best=0,won,blocked;
try { best=Number(localStorage.getItem('2048-best'))||0; } catch (_) {}
function render(fresh) {
  $('#board').replaceChildren();
  board.forEach((row,r)=>row.forEach((value,c)=>{
    const tile=document.createElement('div');
    tile.className='tile'+(value>=128?' large':'')+(value>=16384?' huge':'')+(fresh&&fresh[0]===r&&fresh[1]===c?' fresh':'');
    tile.dataset.value=value; tile.textContent=value||'';
    tile.setAttribute('aria-label',`第 ${r+1} 行，第 ${c+1} 列：${value||'空'}`);
    $('#board').append(tile);
  }));
  $('#score').textContent=score; $('#best').textContent=best;
}
function newGame() {
  board=Array.from({length:4},()=>Array(4).fill(0)); score=0; won=false; blocked=false;
  spawn(board); const fresh=spawn(board);
  $('#overlay').hidden=true; $('#status').textContent='准备好了吗？让数字动起来。'; render(fresh);
}
function showEnd(victory) {
  blocked=true; $('#overlay').hidden=false;
  $('#message').textContent=victory?'2048，达成！':'这局到这里啦';
  $('#detail').textContent=victory?'漂亮！还想挑战更大的数字吗？':`本局得分 ${score}，下一局会更好。`;
  $('#continue').hidden=!victory;
}
function play(direction) {
  if(blocked) return;
  const result=move(board,direction);
  if(!result.changed) return;
  board=result.board; score+=result.score;
  if(score>best) { best=score; try { localStorage.setItem('2048-best',best); } catch (_) {} }
  render(spawn(board));
  $('#status').textContent=result.score?`合并成功！+${result.score} 分`:'继续寻找下一次合并。';
  if(!won&&board.some(row=>row.some(v=>v>=2048))) { won=true; showEnd(true); }
  else if(!canMove(board)) showEnd(false);
}
const keys={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down',a:'left',d:'right',w:'up',s:'down'};
document.addEventListener('keydown',event=>{
  if(event.ctrlKey||event.metaKey||event.altKey) return;
  const direction=keys[event.key]||keys[event.key.toLowerCase()];
  if(direction) { event.preventDefault(); play(direction); }
});
document.querySelectorAll('[data-direction]').forEach(button=>button.addEventListener('click',()=>play(button.dataset.direction)));
$('#restart').addEventListener('click',newGame); $('#again').addEventListener('click',newGame);
$('#continue').addEventListener('click',()=>{ $('#overlay').hidden=true; blocked=false; if(!canMove(board)) showEnd(false); });
let touchStart;
$('#board').addEventListener('pointerdown',event=>{ touchStart=[event.clientX,event.clientY]; $('#board').setPointerCapture(event.pointerId); });
$('#board').addEventListener('pointercancel',()=>{touchStart=null;});
$('#board').addEventListener('pointerup',event=>{
  if(!touchStart) return;
  const dx=event.clientX-touchStart[0],dy=event.clientY-touchStart[1]; touchStart=null;
  if(Math.max(Math.abs(dx),Math.abs(dy))<20) return;
  play(Math.abs(dx)>Math.abs(dy)?(dx>0?'right':'left'):(dy>0?'down':'up'));
});
newGame();
