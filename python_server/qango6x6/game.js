num_squares = 36
const body_rect = document.body.getBoundingClientRect();
const board_size = Math.min(body_rect.height * 0.85, body_rect.width * 0.5);
const board = document.getElementById("board");
board.style.width = board_size + "px";
board.style.height = board_size + "px";
board.style.top = (body_rect.height/2 - board_size/2)+"px";
const tbody = board.children[0];
for (var tr of tbody.children){
    tr.style.height = (board_size/Math.sqrt(num_squares)) + "px";
    for (var td of tr.children){
        td.style.width = (board_size/Math.sqrt(num_squares)) + "px";
        td.style.height = "100%";
    }
}

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