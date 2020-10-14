num_squares = 37

function move_int_to_str(int_move){
    removals = [0,0,3,3,3,8,29,34,34,34]
    for (var i = 0; i<removals.length; i++){
        if (removals[i]>int_move){
            break
        }
    }
    console.log(int_move,i)
    int_move+=i
    return "abcdefg"[int_move % 7]+(parseInt(int_move/7)+1)
}

function get_squares(){
    var tbody = document.getElementById("board").children[0]
    var tds = []
    for (var i = 0; i < tbody.children.length; i++){
        var tr = tbody.children[i]
        for (var j = 0; j < tr.children.length; j++){
            if (tr.children[j].className!="invis"){
                tds.push(tr.children[j])
            }
        }
    }
    return tds
}