const matrix = [
    [8, 1, 6],
    [3, 5, 7],
    [4, 9, 2],
];

const sumArray = arr => arr.reduce((acc, val) => acc + val, 0);

const isMagicSquare = (mat) => {
    const checkSum = sumArray(mat[0]);
    let colsSums = Array.from({length: mat.length}, i => i = 0);
    let diagonalSums = [0,0];
    for (row of mat) {
        // check cols and rows lengths and rows sums
        if (row.length != mat.length || checkSum !== sumArray(row)) {
            console.log(`Row ${row} is not equal to ${checkSum}`);
            return false;
        }

        // create sums of columns
        for (i in row) {
            colsSums[i] += row[i];
        }
        // create diagonals sums
        diagonalSums[0] += row[i];
        diagonalSums[1] += row[row.length - 1 - i];
    }
    // check cols sums
    for (i in colsSums) {
        if (colsSums[i] != checkSum) {
            console.log(`Column number ${i + 1} is not equal to ${checkSum} (${colsSums[i]})`);
            return false;
        }
    }
    // check diagonals sums
    for (i in diagonalSums) {
        if (diagonalSums[i] !== checkSum) {
            console.log(`Diagonal number ${i++} is not equal to ${checkSum} (${diagonalSums[i]})`);
            return false
        }
    }
    return true;
}


// Test cases for non-magic squares

// Example 1: Unequal row sums
const nonMagicSquare1 = [
    [2, 7, 6],
    [9, 5, 1],
    [4, 3, 9]  // The last element should be '8' for this to be a magic square
]; // Row sums differ

// Example 2: Unequal column sums
const nonMagicSquare2 = [
    [8, 1, 6],
    [3, 10, 7],  // Middle column sum is different due to '10'
    [4, 9, 2]
]; // Column sums differ

// Example 3: Unequal diagonal sums
const nonMagicSquare3 = [
    [16, 3, 2],
    [3, 7, 6],
    [4, 5, 8]
]; // Diagonal sums differ

// Example 4: Not a square matrix (2x3 matrix)
const nonMagicSquare4 = [
    [4, 9, 2],
    [3, 5, 7]
]; // Not a square matrix

// Example 5: Square matrix but unequal sums
const nonMagicSquare5 = [
    [5, 9, 1],
    [6, 7, 2],
    [3, 4, 8]
]; // Diagonal and column sums differ

// Example 6: All rows equal, but diagonal unequal
const nonMagicSquare6 = [
    [6, 1, 8],
    [7, 5, 3],
    [2, 9, 4]  // All rows are equal, but diagonals differ
]; // Diagonal sums differ

// Example 7: A valid magic square for comparison
const magicSquare = [
    [8, 1, 6],
    [3, 5, 7],
    [4, 9, 2]
]; // This is a valid 3x3 magic square

// Testing the examples
console.log("Non-magic square 1:", isMagicSquare(nonMagicSquare1));  // Output: false
console.log("Non-magic square 2:", isMagicSquare(nonMagicSquare2));  // Output: false
console.log("Non-magic square 3:", isMagicSquare(nonMagicSquare3));  // Output: false
console.log("Non-magic square 4:", isMagicSquare(nonMagicSquare4));  // Output: false
console.log("Non-magic square 5:", isMagicSquare(nonMagicSquare5));  // Output: false
console.log("Non-magic square 6:", isMagicSquare(nonMagicSquare6));  // Output: false
console.log("Magic square:", isMagicSquare(magicSquare));     

console.log(isMagicSquare(matrix));