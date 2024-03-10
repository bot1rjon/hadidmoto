
let app = new Vue ({
delimiters: [ '[[', ']]'],
el: '#root',
data: {
    cart_products: [],
    no_item: true,
    set_success: true,
    mm_alert_success: false,
    empty_block: false,
    total_quantity: 0
},
mounted() {
    if (JSON.parse(localStorage.getItem('products'))) {
        this.cart_products = JSON.parse(localStorage.getItem('products'))
        const index = this.cart_products.findIndex(item => item.id === null);
        if (index !== -1) {
            this.cart_products.splice(index, 1);
            localStorage.setItem('products', JSON.stringify(this.cart_products))
        }
        let json = {"products": this.cart_products}
        fetch("/cart/get/", {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': csrftoken
                  },
                  body: JSON.stringify(json)
              })
                .then((e) => e.json())
                .then((e) => {
                    this.cart_products = e.cart_products
                    localStorage.setItem('products', JSON.stringify(this.cart_products))
                })
    } else {
        this.no_item = true
    }
    if (JSON.parse(localStorage.getItem('quantity'))) {
        this.quantity = JSON.parse(localStorage.getItem('quantity'))
        const index = this.quantity.findIndex(item => item.id === null);
        if (index !== -1) {
            this.quantity.splice(index, 1);
        }
    }
    if (JSON.parse(localStorage.getItem('total_quantity'))) {
        this.total_quantity = JSON.parse(localStorage.getItem('total_quantity'))
    } 
    if(this.cart_products.length <= 0){
        this.no_item = false
        this.empty_block = true
    } else {
        this.no_item = true
        this.empty_block = false
    }           
    let total_quant = document.querySelector("#total_quant")
    total_quant.innerText = this.total_quantity 

    let marquee = document.querySelectorAll('.marque_check')
},


methods: {
    cart_order_plus(id) {
        const index = this.cart_products.findIndex(item => item.id === id);
        let tt_q = document.querySelector("#total_quantity")
        let total_quant = document.querySelector("#total_quant")
        if (index !== -1) {
            let product = this.cart_products[index]
            product.quantity++
            this.total_quantity++
            if(this.cart_products.length <= 0){
                this.no_item = false
                this.empty_block = true
            } else {
                this.no_item = true
                this.empty_block = false
            }
            localStorage.setItem('products', JSON.stringify(this.cart_products))
            localStorage.setItem('total_quantity', JSON.stringify(this.total_quantity))
            tt_q.innerText = this.total_quantity
            total_quant.innerText = this.total_quantity
        }                

    },
    cart_order_minus(id) {
        const index = this.cart_products.findIndex(item => item.id === id);
        let tt_q = document.querySelector("#total_quantity")
        let total_quant = document.querySelector("#total_quant")
        if (index !== -1) {
            let product = this.cart_products[index]
            product.quantity--
            this.total_quantity--
            if(product.quantity <= 0){
                this.cart_products.splice(index, 1);
            }
            if(this.cart_products.length <= 0){
                this.no_item = false
                this.empty_block = true
            } else {
                this.no_item = true
                this.empty_block = false
            }
            localStorage.setItem('products', JSON.stringify(this.cart_products))
            localStorage.setItem('total_quantity', JSON.stringify(this.total_quantity))
            tt_q.innerText = this.total_quantity
            total_quant.innerText = this.total_quantity
        }                

    },           
    remove_order(id) {
        const index = this.cart_products.findIndex(item => item.id === id);
        let tt_q = document.querySelector("#total_quantity")
        let total_quant = document.querySelector("#total_quant")
        if (index !== -1) {
            let product = this.cart_products[index]
            this.cart_products.splice(index, 1);
            if(this.cart_products.length <= 0){
                this.no_item = false
                this.empty_block = true
            } else {
                this.no_item = true
                this.empty_block = false
            }
            localStorage.setItem('products', JSON.stringify(this.cart_products))
            this.total_quantity = this.cart_products.reduce((total, item) => total + parseInt(item.quantity), 0);
            localStorage.setItem('total_quantity', JSON.stringify(this.total_quantity))
            tt_q.innerText = this.total_quantity
            total_quant.innerText = this.total_quantity
        }                
    },  
    quantity_change(event, id) {
        const index = this.cart_products.findIndex(item => item.id === id);
        let tt_q = document.querySelector("#total_quantity")
        let total_quant = document.querySelector("#total_quant")
        if (index !== -1) {
            let product = this.cart_products[index]
            product.quantity = event.target.value
            if(product.quantity <= 0){
                this.cart_products.splice(index, 1);
            }
            if(this.cart_products.length <= 0){
                this.no_item = false
                this.empty_block = true
            } else {
                this.no_item = true
                this.empty_block = false
            }
            localStorage.setItem('products', JSON.stringify(this.cart_products)) 
            this.total_quantity = this.cart_products.reduce((total, item) => total + parseInt(item.quantity), 0);
            localStorage.setItem('total_quantity', JSON.stringify(this.total_quantity))
            tt_q.innerText = this.total_quantity
            total_quant.innerText = this.total_quantity
        }      
    },
    
    send_order(event) {
        let order_region = document.querySelector("#OrderRegion")         
        let order_name = document.querySelector("#OrderName")         
        let order_phone = document.querySelector("#OrderPhone")    
        let tt_q = document.querySelector("#total_quantity")
        if(order_region.value == ""){order_region.classList.add('error'); order_name.classList.remove('error'); order_phone.classList.remove('error')
        }else if(order_name.value == "") {order_region.classList.remove('error'); order_name.classList.add('error');order_phone.classList.remove('error')
        }else if(order_phone.value == "") {order_region.classList.remove('error'); order_name.classList.remove('error'); order_phone.classList.add('error')
        }else {
            order_region.classList.remove('error'); order_name.classList.remove('error'); order_phone.classList.remove('error')
            let order_url = '/order/send/'
            let orders = JSON.parse(localStorage.getItem('products'))
            let json = {'region': order_region.value,'phone': order_phone.value, 'name': order_name.value, "orders": orders}
            fetch(order_url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(json)
            },)
            .then((e) => e.json())
            .then((e) => {
                this.set_success = false
                this.mm_alert_success = true
                this.no_item = false
                this.empty_block = true
                this.total_quantity = 0
                tt_q.innerText = 0
                localStorage.removeItem('products')
                localStorage.removeItem('total_quantity')
                this.cart_products = []
            })
        }
    },
}
})