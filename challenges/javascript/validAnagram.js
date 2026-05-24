function validAnagram(first, second){
    if(first.length !== second.length) return false;
    let lookup = {};
    for(let i=0; i<first.length; i++) {
        let item = first[i];
        lookup[item] ? lookup[item] += 1 : lookup[item] = 1;
    } 
    for(let i=0; i< second.length; i++){
        let item = second[i];
        if(!lookup[item]) return false;
        else {
            lookup[item] -= 1;
        }
    }
    return true;
}
console.log(validAnagram('nagram', 'angram'));