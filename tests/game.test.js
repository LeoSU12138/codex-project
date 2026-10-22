const {test}=require('node:test');
const assert=require('node:assert/strict');
const {move,spawn,canMove}=require('../web/game.js');
const grid=row=>[row,[0,0,0,0],[0,0,0,0],[0,0,0,0]];
test('tiles merge once and award the correct score without mutating input',()=>{
  const board=grid([2,2,2,2]), result=move(board,'left');
  assert.deepEqual(result.board[0],[4,4,0,0]); assert.equal(result.score,8);
  assert.deepEqual(board[0],[2,2,2,2]);
  assert.deepEqual(move(grid([2,2,4,0]),'left').board[0],[4,4,0,0]);
});
test('gaps and rightward movement',()=>{
  assert.deepEqual(move(grid([2,0,2,4]),'right').board[0],[0,0,4,4]);
  assert.equal(move(grid([2,0,0,0]),'left').changed,false);
});
test('vertical moves and 2048 merge',()=>{
  const board=[[1024,0,0,0],[0,0,0,0],[1024,0,0,0],[0,0,0,0]];
  assert.equal(move(board,'up').board[0][0],2048);
  const result=move(board,'down'); assert.equal(result.board[3][0],2048); assert.equal(result.score,2048);
});
test('game over and full boards with available merges',()=>{
  const board=[[2,4,2,4],[4,2,4,2],[2,4,2,4],[4,2,4,2]];
  assert.equal(canMove(board),false); board[0][0]=4; assert.equal(canMove(board),true);
});
test('spawning respects empty cells and the two possible values',()=>{
  const board=Array.from({length:4},()=>Array(4).fill(2)); assert.equal(spawn(board),null);
  board[2][3]=0; assert.deepEqual(spawn(board,()=>0),[2,3]); assert.equal(board[2][3],2);
  board[2][3]=0; spawn(board,()=>0.95); assert.equal(board[2][3],4);
});
