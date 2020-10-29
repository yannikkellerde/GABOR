export function arr_eq(a, b) {
    return a.length === b.length &&
      a.every((val, index) => val === b[index]);
}
export function arr_in_arr(haystack,needle) {
    var found = false;
    haystack.forEach(el => {
        if (arr_eq(el,needle)){
            found = true;
        }
    });
    return found;
}
export function arr_contains(haystack,needle){
    // Check if array haystack contains the array needle
    return haystack.some(arr => arr_eq(arr,needle));
}
export function arr_set_equal(a,b){
    // Check if the arrays a,b contain exactly the same arrays as elements
    if (a.length!=b.length){
        return false;
    }
    return a.every(arr=>arr_contains(b,arr));
}
export function issubset(a,b){
    // Check if a is a subset of b, with the elements of a and b being array
    return a.every(arr=>arr_contains(b,arr));
}
export function arr_set_search(haystack,needle){
    // Find the index of a 2d array needle in a 3d array haystack while ignoring the order of the first needle dimension
    for (var i=0;i<haystack.length;i++){
        if (arr_set_equal(haystack[i],needle)){
            return i
        }
    }
    return -1
}