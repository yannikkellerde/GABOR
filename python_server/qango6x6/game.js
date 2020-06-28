num_squares = 36

function move_int_to_str(int_move){
    return "abcdef"[int_move % 6]+(parseInt(int_move/6)+1)
}

function get_squares(){
    var tbody = document.getElementById("board").children[0]
    var tds = []
    for (var i = 0; i < tbody.children.length; i++){
        var tr = tbody.children[i]
        for (var j = 0; j < tr.children.length; j++){
            tds.push(tr.children[j])
        }
    }
    return tds
}