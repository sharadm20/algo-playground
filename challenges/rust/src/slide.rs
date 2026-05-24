

pub fn min_window(s: String, t: String) -> String {
let mut freq = vec![0; 128];
for b in t.bytes() { freq[b as usize] += 1; }
let (mut i, mut r, mut c) = (0, 0..0, t.len());
for (j, b) in s.bytes().enumerate() {
  if freq[b as usize] > 0 { c -= 1; }
  freq[b as usize] -= 1;
  while c == 0 {
    if j - i + 1 < r.len() || r.len() == 0 { r = i..j + 1; }
    let a = s.as_bytes()[i] as usize;
    freq[a] += 1; if freq[a] > 0 { c += 1; }
    i += 1;
  }
}
s[r].into()
}

use std::collections::{HashMap, HashSet};
pub fn find_subarrays(nums: &[i32], k: i32) -> i32 {
  let mut ans = 0;
  let mut sum = 0;
  let mut map = HashMap::new();
  map.insert(0, 1);

  for &num in nums {
      sum += num;
      if let Some(&count) = map.get(&(sum - k)) {
          ans += count;
      }
      *map.entry(sum).or_insert(0) += 1;
  }
  ans
}

pub fn is_valid_sudoku(board: Vec<Vec<char>>) -> bool {
  let mut seen = HashSet::new();
  for i in 0..9{
    for j in 0..9{
      let cur = board[i][j].to_string();
      if cur != "." {
        let row_key = format!("{} found in row {}", cur, i);
        let col_key = format!("{} found in col {}", cur, j);
        let box_key = format!("{} found in box {}-{}", cur, i / 3, j / 3);

        if !seen.insert(row_key) || !seen.insert(col_key) || !seen.insert(box_key) {
            return false;
        }
      }
    }
  }
  true
}

pub fn is_valid_sudoku_sec(board: Vec<Vec<char>>) -> bool {
  //Determine if a 9 x 9 Sudoku board is valid. 
  
  // Only the filled cells need to be validated according to the following rules:

  // Each row must contain the digits 1-9 without repetition.
  // Each column must contain the digits 1-9 without repetition.
  // Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.

  // A Sudoku board (partially filled) could be valid but is not necessarily solvable. 
  // Only the filled cells need to be validated according to the mentioned rules. 

  // SOLUTION A:

  // 1 array for row that memoizes 1 - 9 using respective number as index
  // 1 arrays for each 3x3 cell before reset. current_col = base count. reset current_col every 3 rows. reset arrays
  // go row by row -> if number not in memo, add. if number in memo, return false. 
  // then check if in 3x3 cell, same again.
  
  // worst case should be o(n)
  // avg case should be o(n)


      let mut boxs: [[u8; 9]; 3] = [[0; 9]; 3];

      let mut rows: [[u8; 9]; 9] = [[0; 9]; 9];
      let mut cols: [[u8; 9]; 9] = [[0; 9]; 9];

      for x in (0..9) {
          for y in (0..9) {
              if (board[x][y] != '.') {
  
                  let current_value = ((board[x][y]).to_digit(10).unwrap() - 1) as usize;
                  if (cols[y][current_value] == 1) {
                      return false;
                  } else {
                      cols[y][current_value] = 1;
                  }
  
                  if (rows[x][current_value] == 1) {
                      return false;
                  } else {
                      rows[x][current_value] = 1;
                  }
  
                  let current_cell_index = y / 3;
  
                  if (boxs[current_cell_index][current_value] == 1) {
                      return false;
                  } else {
                      boxs[current_cell_index][current_value] = 1;
                  }
              }
          }


          if ((x + 1) % 3 == 0) {
              boxs = [[0; 9]; 3];
          }
      }

      return true;
  }

  enum Direction {
    Up,
    Down, 
    Left,
    Right,
  }
pub fn spiral_order(matrix: Vec<Vec<i32>>) -> Vec<i32> {
  // use enum
  let mut ans = vec![];
  let mut matrix = matrix;
  let mut dir = Direction::Right;
  let mut round = 0;  
  let mut row = 0;
  let mut col = 0;
  for _ in 0..matrix.len() * matrix[0].len() {
    ans.push(matrix[row][col]);
      match dir {
        Direction::Up => {
          if row == round + 1 {
            col += 1;
            dir = Direction::Right;
            round += 1;
          } else {
            row -= 1;
          }
        }
        Direction::Right => {
          if col + 1 = matrix[0].len() - round{
            row += 1;
            dir = Direction::Down;
          } else {
            col += 1;
          }
      }
      Direction::Down => {
        if row + 1 == matrix.len() - round {
          col -= 1;
          dir = Direction::Left;
        } else {
          row += 1;
        }
      }
      Direction::Left => {
        if col == round {
          row -= 1;
          dir = Direction::Up;
        } else {
          col -= 1;
        }
      }
    }
  }
  ans
}
pub fn merge(intervals : Vec<Vec<i32>) -> Vec<Vec<i32>>{
    let mut ans :Vec<Vec<i32>> = Vec::new();
    let mut intervals = intervals;
    intervals.sort();
    for interval in intervals{
        if(ans.is_empty() || ans.last()[1] < interval[0] {
            ans.add(interval);
         }else {
             ans.last_mut().unwrap()[1] = ans.last_mut().unwrap()[1].max(interval[1]);
             }
        }
    ans
 }
