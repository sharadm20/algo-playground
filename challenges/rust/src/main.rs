mod slide;
fn main() {
    let mut nums = vec![-1,0,1,2,-1,-4];
    nums.sort(); // -4 -1 -1 0 1 2
    let s = String::from("barfoofoobarthefoobarman");
    let words = vec!["bar".to_string(),"foo".to_string(),"the".to_string()];
    let res2 = three_sum(nums);
    let s2 = String::from("ADOBECODEBANC");
    let t = String::from("ABC");
    let out = slide::min_window(s2,t);
   let res = find_substring(s, words);
    println!("{:?}", res);
    println!("{:?}", res2);
    println!("{}", out);
    let k = 2;
    let arr = vec![1,1,1];
    let result = slide::find_subarrays(&arr, k);
    println!("Number of subarrays with sum equal to {}: {}", k, result);
 }
// find three number such that their sum is zero
fn three_sum(nums: Vec<i32>) -> Vec<Vec<i32>> {
       let mut result = Vec::new();
       for (i, &cur) in nums.iter().enumerate(){
        if cur > 0 { break; } // for avoiding repeat only pivot negative integers for x
        if i > 0 && cur == nums[i - 1] {
            // skip same/duplicate integers
            continue;
        }
        let (mut lhs, mut rhs) = (i + 1, nums.len()-1); // set left pointer and right pointer

        while lhs < rhs { // iterate till left pointer meets right pointer
            let sum = cur + nums[lhs] + nums[rhs];
            if sum > 0{ //if sum is bigger than zero we need to decrease right pointer to choose low value because of sorted array
                rhs -= 1;
            }  else if sum < 0 { // if sum below zero then increase left pointer
                lhs += 1;
            } else { // push the value to result when sum is found and increment left decrement right for next sum if exist
                result.push(vec![cur, nums[lhs], nums[rhs]]);
                lhs += 1;
                rhs -= 1;
                while nums[lhs] == nums[lhs-1] && lhs < rhs { //increment left pointer if left and left-1 has same value and left is less than right
                    lhs += 1;
                }
            }
        }
    }
        result //return
}
use std::collections::HashMap;

pub fn find_substring(s: String, words: Vec<String>) -> Vec<i32> {
    // Preparation
    let string_bytes = s.as_bytes();
    let string_size = s.len();
    let word_size = words[0].len();

    if word_size > string_size {
        return vec![];
    }

    // Create a map where each word is used as index, as is increment ed with a counter
    let mut map = words.iter().fold(HashMap::<&[u8], (usize, usize)>::new(), |mut map, word| {
        map.entry(word.as_bytes()).or_default().0 += 1;
        map
    });

    // Flag to control each new map run
    let mut new_map = false;
    let mut ans = vec![];

    for idx in 0..word_size {
        if new_map {
            map.iter_mut().for_each(|(_, value)| value.1 = 0);
            new_map = false;
        }
        // Start Sliding Window
        let (mut left, mut right) = (idx, idx);
        
        
        while right <= string_size - word_size {
            println!("left:{} right:{}", left, right);
            // Check if the current right pos, has a full matching word (right + word_size)
            println!("{:?}", &string_bytes[right..right + word_size]);
            match map.get_mut(&string_bytes[right..right + word_size]) {
                None => {
                    right += word_size;
                    left = right;
                    if new_map {
                        map.iter_mut().for_each(|(_, value)| value.1 = 0);
                        new_map = false;
                    }
                }
                Some(right_val) => {
                    right_val.1 += 1;
                    right += word_size;
                    new_map = true; 
                    println!("map=={:?}", right_val);
                    if right_val.1 > right_val.0 {
                        loop {
                            let left_val = map.get_mut(&string_bytes[left..left + word_size]).unwrap();
                            left += word_size;
                            left_val.1 -= 1;
                            if left_val.0 == left_val.1 {
                                break;
                            }
                        }
                    }
                }
            }

            if right - left == words.len() * word_size {
                ans.push(left as i32);
                map.get_mut(&string_bytes[left..left + word_size]).unwrap().1 -= 1;
                left += word_size;
            }
        }
    }
    ans
}