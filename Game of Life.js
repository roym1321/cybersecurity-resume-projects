// The Game of Life is a simulation of how a population of creatures evolves from one generation to the next, based on a set of simple rules.
// This colony is described by a matrix of a user determined size, where each cell is either populated by a 
// creature (marked by an asterisk '*'), or vacant. As with any matrix, each cell can have 8 neighboring cells at the most.



var gBoard = [
    ['*','*',' ','*','*',' ',' ',' ',' ','*'],
    ['*','*',' ','*','*',' ',' ',' ',' ',' '],
    ['*','*',' ',' ',' ','*','*','*',' ',' '],
    ['*','*',' ',' ',' ','*','*','*',' ',' '],
    [' ',' ',' ',' ',' ','*','*',' ',' ','*'],
    [' ',' ','*',' ',' ',' ',' ',' ','*','*'],
    [' ',' ','*',' ',' ',' ',' ',' ',' ',' '],
    ['*',' ',' ',' ',' ',' ','*',' ',' ','*'],
    ['*',' ',' ',' ',' ',' ','*',' ',' ','*']
]

var board2 = [
    ['*','*',' ',' ',' '],
    ['*','*',' ',' ','*'],
    [' ',' ','*',' ',' '],
    ['*',' ',' ',' ',' '],
]
var interationCount = 1;

const findSurroundingMonsters = (board, i, j) => {
    let monstersCount = 0;
    let surroundingMonstersIndexes = [
                            [i - 1,j - 1],[i - 1,j],[i - 1,j + 1],
                            [i,j - 1],[i,j + 1],
                            [i + 1,j - 1],[i + 1,j],[i + 1,j + 1]
                        ];
    for (const [i, j] of surroundingMonstersIndexes) {
        if (i >= 0 && j >= 0 && i < board.length && j < board[i].length) {
            board[i][j] == '*' ? monstersCount += 1 : null;
        }
    }
    return monstersCount;
}


const runGeneration = (board) => {
    let newBoard = board.slice();
    for (let i in board) {
        i = parseInt(i);
        let row = board[i];
        for (let j in row){
            j = parseInt(j);
            const monstersCount = findSurroundingMonsters(board, i, j);
            if ((2 < monstersCount && monstersCount < 6)) {
                newBoard[i][j] = '*';
            } else {
                newBoard[i][j] = ' ';
            }
        }
    }
    return newBoard;
}


const renderBoard = (board) => {
    let renderedBoard = `Generation number ${interationCount}\n`;
    interationCount++;
    for (row of board){
        renderedBoard += `|${row.join('|')}|\n`;
    }
    console.log(renderedBoard);
}

const play = () => {
    gBoard = runGeneration(gBoard);
    renderBoard(gBoard);
}

renderBoard(gBoard);
intervalID = setInterval(play, 1000);