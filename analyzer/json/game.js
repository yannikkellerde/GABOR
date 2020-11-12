function set_sizes(){
    const body_rect = document.body.getBoundingClientRect();
    const board_size = Math.min(body_rect.height * 0.85, body_rect.width * 0.5);
    const sq_size = Math.min(board_size/config.cols,board_size/config.rows);
    const board = document.getElementById("board");
    board.style.top = (body_rect.height/2 - board_size/2)+"px";
    const tbody = board.children[0];
    for (var tr of tbody.children){
        tr.style.height = sq_size + "px";
        for (var td of tr.children){
            td.style.width = sq_size + "px";
            td.style.height = sq_size + "px";
        }
    }
}
function display_board(){
    const body_rect = document.body.getBoundingClientRect();
    const board_size = Math.min(body_rect.height * 0.85, body_rect.width * 0.5);
    const sq_size = Math.min(board_size/config.cols,board_size/config.rows);
    const tbody = document.getElementById("board").children[0]
    tbody.innerHTML = "";
    var tds = [];
    for (var i=0;i<config.sq_colors.length;i++){
        var sq_row = config.sq_colors[i];
        const tr = document.createElement("tr");
        var list_of_tds = []
        for (var j=0;j<sq_row.length;j++){
            var sq_col = sq_row[j]
            const td = document.createElement("td");
            td.style.width = td.style.height = sq_size+"px";
            td.setAttribute("data-row",i);
            td.setAttribute("data-column",j);
            if (sq_col=="deleted"){
                td.className = "deleted";
            }
            else{
                td.style.background = sq_col;
                td.className = "square";
            }
            list_of_tds.push(td);
            tr.appendChild(td);
        }
        tds.push(list_of_tds);
        tbody.appendChild(tr);
    }
}
export function move_int_to_str(int_move){
    var removals = config.deleted;
    for (var i = 0; i<removals.length; i++){
        if (removals[i]>int_move){
            break
        }
    }
    int_move+=i
    return "ABCDEFGHJKLMNOPQRSTUVWXYZ"[int_move % config.cols]+(parseInt(int_move/config.cols)+1)
}
export function get_squares(){
    const tbody = document.getElementById("board").children[0]
    var tds = []
    for (var i = 0; i < tbody.children.length; i++){
        var tr = tbody.children[i]
        for (var j = 0; j < tr.children.length; j++){
            if (tr.children[j].className!="deleted"){
                tds.push(tr.children[j])
            }
        }
    }
    return tds
}
export function my_post(data){
    config=data;
    num_squares = config.squares;
    display_board();
    set_sizes();
    var squares = get_squares();
    var position = new Array(num_squares).fill(0);
    var position_hist = [position];
    return [num_squares,squares,position,position_hist]
}

var config;
var num_squares;

export function load_game(){
    config = {};
    num_squares = 0;
    return [num_squares,false];
}
