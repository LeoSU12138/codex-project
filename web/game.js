(function(root) {
  function move(board, direction) {
    if (!['left','right','up','down'].includes(direction)) throw Error('Invalid direction');
    const next = board.map(row => row.slice());
    let score = 0;
    for (let line=0; line<4; line++) {
      const positions = Array.from({length:4}, (_,i) => direction==='left' ? [line,i] : direction==='right' ? [line,3-i] : direction==='up' ? [i,line] : [3-i,line]);
      const values = positions.map(([r,c]) => board[r][c]).filter(Boolean), merged=[];
      for (let i=0; i<values.length; i++) {
        if (values[i]===values[i+1]) { merged.push(values[i]*2); score+=values[i]*2; i++; }
        else merged.push(values[i]);
      }
      positions.forEach(([r,c],i) => { next[r][c]=merged[i]||0; });
    }
    return {board:next, score, changed:next.some((row,r)=>row.some((v,c)=>v!==board[r][c]))};
  }
  function spawn(board, random=Math.random) {
    const empty=[];
    board.forEach((row,r)=>row.forEach((v,c)=>{if(!v) empty.push([r,c]);}));
    if (!empty.length) return null;
    const [r,c]=empty[Math.floor(random()*empty.length)];
    board[r][c]=random()<0.9 ? 2 : 4;
    return [r,c];
  }
  function canMove(board) { return ['left','right','up','down'].some(d=>move(board,d).changed); }
  const rules={move,spawn,canMove};
  if (typeof module!=='undefined' && module.exports) module.exports=rules;
  else root.Game2048=rules;
})(globalThis);
