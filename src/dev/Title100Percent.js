var divs = [...document.querySelectorAll("span")];

var highestItem = [];
var highestSize = 0;
var fontSize = 0;
var content = "";

// Load all
divs.forEach(function(item) {
    
    fontSize = parseInt(window.getComputedStyle(item, null).getPropertyValue('font-size'));
    content = item.textContent;

    if (fontSize >= 10 && content.length > 5) {
        highestItem.push({
            "font_size": fontSize,
            "content": content
        });
    }

});

function compare( a, b ) {
    if ( a.font_size < b.font_size ){
        return 1;
    }
    if ( a.font_size > b.font_size ){
        return -1;
    }
    return 0;
}
highestItem.sort(compare);

// No duplication array
var noDuplicated = [];

// Delete duplicate content
highestItem.forEach(el => {
    if (!noDuplicated.some(e => e.content == el.content)) {
        noDuplicated.push(el);
    }
});

// console.log(highestItem);

highestSize = highestItem[0].font_size
// console.log("highestSize: " + highestSize);

// Les colles
var res = "";
highestItem.forEach(stuck => {
    if (stuck.font_size == highestSize) {    
        res += stuck.content;
    }
});
res = res.replace(new RegExp('\n','g'), ' ');

// Enleve les saut de ligne
console.log(res);