var gnums = [];

const resetMums = () => {
    let arr = [];
    for (let i = 1; i <= 99; i++) {
        arr.push(i);
    }
    gnums = arr
}

const drawNum = () => {
    while (true) {
        let drawedNum = Math.floor(Math.random() * 99) + 1;
        if (gnums.includes(drawedNum)) {
            gnums.splice(gnums.indexOf(drawedNum), 1);
            return drawedNum;
        }
    }
};

const markBoard = (player, calledNum) => {
    for (row of player.board) {
        let completedRow = row.every(n => n.isHit);
        for (num of row) {
            if (num.value == calledNum) {
                num.isHit = true;
                player.hitCount += 1;
                break;
            }
        }
        if (row.every(n => n.isHit) && !completedRow) {
            console.log(`${player.name} has completed a row!`);
            printBingoBoard(player.board);
            break;
        }
    }
};


const checkBingo = (player) => {
    if (player.hitCount === 36) {
        return true;
    }
    return false;
};

function playBingo(){
    resetMums();
    var isVictory = false;
    var intervalID;

    function playTurn(){
        var calledNum = drawNum();
        console.log(`--------------Number ${calledNum}!--------------`)
        for(var i = 0; i < gPlayers.length && !isVictory; i++){
            var player = gPlayers[i];
            markBoard(player, calledNum);
            isVictory = checkBingo(player);
            if (isVictory) {
                console.log(`Player ${player.name} has won`);
                clearInterval(intervalID);
                return;
            }
        }   
    }
    intervalID = setInterval(playTurn, 15);
}    

const createBingoBoard = () => {
    resetMums();
    let newBoard = [
        [{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false}],
        [{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false}],
        [{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false}],
        [{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false}],
        [{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false}],
        [{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false},{value:0, isHit: false}]
    ];
    let usedNumbers = [];
    for (row of newBoard) {
        for (num of row) {
            while (true) {
                let newNumber = Math.floor(Math.random() * 99) + 1;
                if (!usedNumbers.includes(newNumber)) {
                    usedNumbers.push(newNumber);
                    num.value = newNumber;
                    break;
                }
            }
        }
    }
    return newBoard;
}

const printBingoBoard = (board) => {
    let printableBoard = [
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]
    ];
    for (const [i, row] of board.entries()) {
        for (const [j, num] of row.entries()) {
            printableBoard[i][j] = (num.isHit) ? 'VV': (num.value > 9) ? `${num.value}` : `0${num.value}`;
        }
    }
    console.log(` B | I | N | G | O\n------------------`)
    console.log(printableBoard.join('\n'));
}

var gPlayers = [
    {name: 'John', hitCount: 0, board: createBingoBoard()},
    {name: 'Dana', hitCount: 0, board: createBingoBoard()},
    {name: 'Korg', hitCount: 0, board: createBingoBoard()},
]

console.clear();

playBingo();
