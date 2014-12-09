jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "monthYear-pre": function ( a ) {
    a = a.replace(/<font.*>/, "");
    a = a.replace(/<\/font.*>/, "");
    return new Date(a);
    },
 
    "monthYear-asc": function ( a, b ) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },
 
    "monthYear-desc": function ( a, b ) {
        return ((a < b) ? 1 : ((a > b) ?  -1 : 0));
    }
    } );
