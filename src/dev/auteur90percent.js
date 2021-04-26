var divs = [...document.querySelectorAll("div span")];

var highestItem = [];
var highestSize = 0;
var fontSize = 0;
var i=0

// Load all
divs.forEach(function(item) {

    fontSize = parseInt(window.getComputedStyle(item, null).getPropertyValue('font-size'));

    if (fontSize >= highestSize && item.textContent.length >17 && item.textContent.length < 120) {

        highestSize = fontSize;



    }

    if (fontSize<highestSize && fontSize>10 && item.textContent.length < 40 && item.textContent.length > 10 && i<3) {

        highestItem.push({
            "fontSize": fontSize,
            "content": item.textContent,
            "item": item
        });
        console.log(highestSize);
        console.log(item);    
        i++;    
    }

});

// Sort by fontSize
highestItem = highestItem.sort((a, b) => b.fontSize - a.fontSize);

// No duplication array
var noDuplicated = [];

// Delete duplicate content
highestItem.forEach(el => {
    if (!noDuplicated.some(e => e.content == el.content) && el.content.includes("\n")) {
        noDuplicated.push(el);
    }
});

console.log(highestItem);

// Les colles
var res = "";
highestItem.forEach(i => {
    if (i.fontSize = highestSize) {    
        res += i.content;
    }
});

// Enleve les saut de ligne
console.log(res.replace(new RegExp('\n','g'), ' '));