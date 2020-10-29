export function find_rows(row_len,num_rows,num_cols,deleted){
    var wps = []
    for (var y=0;y<num_rows;y++){
        for (var x=0;x<=num_cols-row_len;x++){
            var dead = false;
            var wp = [];
            for (var k=x;k<x+row_len;k++){
                if (deleted[y][k]=="deleted"){
                    dead = true;
                    break;
                }
                wp.push([y,k])
            }
            if (!dead){
                wps.push(wp);
            }
        }
    }
    return wps
}
export function find_columns(col_len,num_rows,num_cols,deleted){
    var wps = [];
    for (var x=0;x<num_cols;x++){
        for (var y=0;y<=num_rows-col_len;y++){
            var dead = false;
            var wp = [];
            for (var k=y;k<y+col_len;k++){
                if (deleted[k][x]=="deleted"){
                    dead = true;
                    break;
                }
                wp.push([k,x])
            }
            if (!dead){
                wps.push(wp);
            }
        }
    }
    return wps
}
export function find_first_diagonals(diag_len,num_rows,num_cols,deleted){
    var wps = [];
    for (var y=diag_len-1;y<num_rows;y++){
        for (var x=0;x<=num_cols-diag_len;x++){
            var dead=false;
            var wp = [];
            for (var k=0;k<diag_len;k++){
                let mx = x+k;
                let my = y-k;
                if (deleted[my][mx]=="deleted"){
                    dead = true;
                    break;
                }
                wp.push([my,mx]);
            }
            if (!dead){
                wps.push(wp);
            }
        }
    }
    return wps
}
export function find_second_diagonals(diag_len,num_rows,num_cols,deleted){
    var wps = [];
    for (var y=0;y<=num_rows-diag_len;y++){
        for (var x=0;x<=num_cols-diag_len;x++){
            var dead=false;
            var wp = [];
            for (var k=0;k<diag_len;k++){
                let mx = x+k;
                let my = y+k;
                if (deleted[my][mx]=="deleted"){
                    dead = true;
                    break;
                }
                wp.push([my,mx]);
            }
            if (!dead){
                wps.push(wp);
            }
        }
    }
    return wps
}
export function find_squares(num_rows,num_cols,deleted){
    var wps = [];
    for (var y=0;y<num_rows-1;y++){
        for (var x=0;x<num_cols-1;x++){
            var dead=false;
            var wp = [];
            for (var mx=x;mx<=x+1;mx++){
                for (var my=y;my<=y+1;my++){
                    if (deleted[my][mx]=="deleted"){
                        dead = true;
                        break;
                    }
                    wp.push([my,mx]);
                }
            }
            if (!dead){
                wps.push(wp);
            }
        }
    }
    return wps
}