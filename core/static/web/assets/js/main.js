$('.owl-sale-products').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    autoplay:true,
    autoplayTimeout:5000, // Set autoplay timeout in milliseconds (e.g., 2000 for 2 seconds)
    autoplayHoverPause:true,
    responsive:{
        0:{
            items: 1.9
        },
        710:{
            items: 2.9
        },
        997:{
            items:4
        }
    }
})

$('.owl-smillar-products').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    autoplay:true,
    autoplayTimeout:5000, // Set autoplay timeout in milliseconds (e.g., 2000 for 2 seconds)
    autoplayHoverPause:true,
    responsive:{
        0:{
            items: 1.9
        },
        530:{
            items: 2.5
        },
        650:{
            items: 2.9
        },
        800:{
            items: 3.9
        },
        997:{
            items:2.9
        }
    }
})


$('.owl-foot-sliders').owlCarousel({
    pagination:false,
    loop:true,
    margin:0,
    autoplay:true,
    autoplayTimeout:5000, // Set autoplay timeout in milliseconds (e.g., 2000 for 2 seconds)
    autoplayHoverPause:true,
    responsive:{
        0:{
            items: 1
        }
    }
})

$('.owl-sliders').owlCarousel({
    pagination:false,
    loop:true,
    margin:0,
    autoplay:true,
    autoplayTimeout:5000, // Set autoplay timeout in milliseconds (e.g., 2000 for 2 seconds)
    autoplayHoverPause:true,
    responsive:{
        0:{
            items: 1
        }
    }
})



if(document.querySelector('#nav-list')){
    document.querySelector('#nav-list').addEventListener('click', () => {
        if(document.querySelector('.list-menu-dropdown-show')) {
            document.querySelector('#show-list-menu-dropdown').classList.remove('list-menu-dropdown-show')
        }else{
            document.querySelector('#show-list-menu-dropdown').classList.add('list-menu-dropdown-show')
            document.querySelector('#show-nav-menu-dropdown').classList.remove('nav-menu-dropdown-show')
        }
    })
}

if(document.querySelector('#nav-menu')){
    document.querySelector('#nav-menu').addEventListener('click', () => {
        if(document.querySelector('.nav-menu-dropdown-show')) {
            document.querySelector('#show-nav-menu-dropdown').classList.remove('nav-menu-dropdown-show')
        }else{
            document.querySelector('#show-nav-menu-dropdown').classList.add('nav-menu-dropdown-show')
            document.querySelector('#show-list-menu-dropdown').classList.remove('list-menu-dropdown-show')
        }
    })
}


if(document.querySelector("#sserc")){
    function filterFunction() {
        input = document.querySelector("#sserc");
        filter = input.value.toLowerCase().replaceAll(" ", '');
        p = document.querySelectorAll(".search_title");
        box = document.querySelector('#show-search-dropdown')
        p.forEach(i => {
            search = i.innerText.replaceAll(" ", '');
            if (search.toLowerCase().indexOf(filter) > -1) {
                i.parentElement.classList.remove('d-none')
            } else {
                i.parentElement.classList.add('d-none')
            } 
        });
    }
    document.querySelector("#sserc").addEventListener('input', () => {
        filterFunction()
        c = 0
        parent_title = document.querySelectorAll(".parent-title")
        parent_title.forEach(a => {
            if(a.classList.value.includes('d-none')){
                // 
            }
            else {
                c += 1
            }
        })
        if(c == 0){
            document.querySelector('#show-search-dropdown').classList.add('show-search-dropdown')
        }else {
            document.querySelector('#show-search-dropdown').classList.remove('show-search-dropdown')
        }

        document.querySelector('#show-search-dropdown').classList.add('show-search-dropdown')
        if(document.querySelector("#sserc").value.length == 0){
            document.querySelector('#show-search-dropdown').classList.remove('show-search-dropdown')
        }
    })
}

if(document.querySelector("#FilterRegion")){
    let change_region = document.querySelector('#FilterRegion')
    let change_district = document.querySelector('#FilterDistrict')
    let districts = document.querySelectorAll('.CitySelect')
    let filter_item = document.querySelectorAll('.FilterClassItem')
    districts.forEach(item => {
        if (change_region.value == item.dataset.id) {
            item.classList.remove('d-none')
        } else if (change_region.value == "" && change_district.value == "") {
                item.classList.remove('d-none')
        } else {
            item.classList.add('d-none')
        }
    });
    change_region.addEventListener('change', ()=> {
        filter_item.forEach(item => {
            if (change_region.value == item.dataset.region) {
                item.classList.remove('d-none')
            } else if (change_region.value == "") {
                item.classList.remove('d-none')
            }  else if (change_region.value == "" && change_district.value == "") {
                item.classList.remove('d-none')
            }  else if (change_region.value == "" && change_district.value == item.dataset.city) {
                item.classList.remove('d-none')
            }  else {
                item.classList.add('d-none')
            }
        })
        districts.forEach(item => {
            if (change_region.value == item.dataset.id) {
                item.classList.remove('d-none')
            } else if (change_region.value == "") {
                item.classList.remove('d-none')
            } else {
                item.classList.add('d-none')
            }
        })
    })
    
    change_district.addEventListener('change', ()=> {
        filter_item.forEach(item => {
            if (change_region.value == item.dataset.region && change_district.value == item.dataset.city) {
                item.classList.remove('d-none')
            } else if (change_region.value == "" && change_district.value == item.dataset.city ) {
                item.classList.remove('d-none')
            }  else if (change_region.value == "" && change_district.value == "") {
                item.classList.remove('d-none')
            }  else if (change_region.value == item.dataset.region && change_district.value == "") {
                item.classList.remove('d-none')
            }   else {
                item.classList.add('d-none')
            }
        })
    })
}


// if($("#OrderSendButton").length){
//     $("#OrderSendButton").click(() => {
//         if($("#OrderRegion").val() == "") {
//             $("#OrderRegion").addClass("error"); $("#OrderPhone").removeClass("error");$("#OrderName").removeClass("error") 
//         }else if($("#OrderName").val() == "") {
//             $("#OrderRegion").removeClass("error"); $("#OrderPhone").removeClass("error"); $("#OrderName").addClass("error") 
//         }else if($("#OrderPhone").val() == "") {
//             console.log("hello");
//             $("#OrderRegion").removeClass("error");$("#OrderPhone").addClass("error");$("#OrderName").removeClass("error") 
//         }else {
//             $("#OrderRegion").removeClass("error"); $("#OrderPhone").removeClass("error"); $("#OrderName").removeClass("error") 
//             // let url = '/order/send/'
// 			let json = {'name': $("#OrderName").val(), 'phone': $("#OrderPhone").val(), 'region': $("#OrderRegion").val()}
//             console.log(json);

// 			// fetch(url, {
// 			// 	method: 'POST',
// 			// 	headers: {
// 			// 		'Content-Type': 'application/json',
// 			// 		'X-CSRFToken': csrftoken
// 			// 	},
// 			// 	body: JSON.stringify(json)
// 			// },).then((resp) => resp.json())
//             // .then((data) => {
//             //     console.log(data);
//             //     $("#sent-success").addClass('d-none')
//             //     $("#mm-alert-success").removeClass("d-none")
//             // })
//                 $("#sent-success").addClass('d-none')
//                 $("#mm-alert-success").removeClass("d-none")
//                 localStorage.removeItem('products')
//                 localStorage.removeItem('total_quantity')
//                 setInterval(function() {
//                     location.reload();
//                 }, 3000);
                
//         }
//     })
// }

// Add to cart

    let products = [{"id": null}]
    let total_quantity = 0
    
    let tt_q = document.querySelector("#total_quantity")
    if (JSON.parse(localStorage.getItem('products'))) {
        products = JSON.parse(localStorage.getItem('products'));
    } else {
        localStorage.setItem('products', JSON.stringify(products))
    }
    if (JSON.parse(localStorage.getItem('total_quantity'))) {
        total_quantity = JSON.parse(localStorage.getItem('total_quantity'));
    } else {
        localStorage.setItem('total_quantity', JSON.stringify(total_quantity))
    }
    localStorage.setItem('total_quantity', JSON.stringify(total_quantity))
    let add_cart = document.querySelectorAll('.addToCart')
    if(tt_q <= 0){
        tt_q.classList.add("d-none")
    }else{
        tt_q.innerText = total_quantity
    }
    add_cart.forEach(add => {
        add.addEventListener("click",(a)=> {
            let productIndex = products.findIndex(product => parseInt(product.id) === parseInt(add.dataset.id));
            if (productIndex !== -1) {
                let product = products[productIndex]
                product.quantity++
                total_quantity++
                tt_q.innerText = total_quantity
                localStorage.setItem('products', JSON.stringify(products))
                localStorage.setItem('total_quantity', JSON.stringify(total_quantity))
            } else {
                    let arr = {
                        "id": parseInt(add.dataset.id),
                        "title": add.dataset.title,
                        "subtitle": add.dataset.subtitle,
                        "quantity": 1,
                        "price": add.dataset.price,
                        "old_price": add.dataset.old_price,
                        "img": add.dataset.img,
                        "company": add.dataset.company,
                        "discount": add.dataset.discount,
                    }
                    products.push(arr)
                    total_quantity++
                    tt_q.innerText = total_quantity
                    localStorage.setItem('total_quantity', JSON.stringify(total_quantity))
                    localStorage.setItem('products', JSON.stringify(products))
            }
        })
    });


    let marquee = document.querySelectorAll('.marque_check')
    setInterval(function() {
        marquee.forEach(m => {
            if(m.innerText.length >=17){
                m.classList.add('tttmm')
            }
        })
    }, 4000);