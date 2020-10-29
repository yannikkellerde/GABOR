export function arr_eq(a, b) {
    // Check if two array are equal
    return a.length === b.length &&
      a.every((val, index) => val === b[index]);
}
export function arr_in_arr(haystack,needle) {
    // Check if an array is in a list of arrays
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
export function filter_dups(arr){
    // Remove duplicates of an array of arrays
    var known = [];
    for (var i=arr.length-1;i>-1;i--){
        if (arr_set_search(known,arr[i])!=-1){
            arr.splice(i,1);
        }
        else{
            known.push(arr[i]);
        }
    }
}