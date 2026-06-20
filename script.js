
const products = [{"name": "Essential Tee", "category": "Apparel", "price": "₹799", "image": "assets/tee.jpg", "desc": "Premium cotton essential."}, {"name": "Minimal Leather Wallet", "category": "Accessories", "price": "₹999", "image": "assets/wallet.jpg", "desc": "Refined everyday carry."}, {"name": "Linen Henley Shirt", "category": "Apparel", "price": "₹1,699", "image": "assets/henley.jpg", "desc": "Breathable luxury linen."}, {"name": "Terrarium Kit", "category": "Lifestyle", "price": "₹649", "image": "assets/terrarium.jpg", "desc": "Build your ecosystem."}, {"name": "Scented Candle Set", "category": "Home Living", "price": "₹899", "image": "assets/candles.jpg", "desc": "Curated aroma trio."}, {"name": "Canvas Tote Bag", "category": "Accessories", "price": "₹1,299", "image": "assets/tote.jpg", "desc": "Minimal everyday tote."}, {"name": "Japandi Diffuser", "category": "Home Living", "price": "₹2,499", "image": "assets/diffuser.jpg", "desc": "Atmospheric diffuser."}, {"name": "Hexagon Sunglasses", "category": "Accessories", "price": "₹1,499", "image": "assets/sunglasses.jpg", "desc": "Modern geometric frame."}, {"name": "Charcoal Hoodie", "category": "Apparel", "price": "₹1,999", "image": "assets/hoodie.jpg", "desc": "Heavyweight comfort."}];

function render(arr){
productGrid.innerHTML = arr.map(x => `
<div class="product">
<img loading="lazy" src="${x.image}" alt="${x.name}">
<div style="padding:15px">
<h3>${x.name}</h3>
<p>${x.desc}</p>
<b class="price">${x.price}</b>
<div style="margin-top:10px">♡ <button>Add to Cart</button></div>
</div>
</div>`).join('');
}

render(products);

document.addEventListener('click',e=>{
if(e.target.dataset.filter){
const f=e.target.dataset.filter;
render(f==='all' ? products : products.filter(x=>x.category===f));
}
});

function subscribe(){
msg.innerText='✓ Subscription successful';
}

// ===== CLOUD FUNCTION CONTACT HANDLER =====
const CONTACT_FUNCTION_URL = 'https://handle-contact-v2-927825491730.asia-south1.run.app';

function sendForm(e){
e.preventDefault();
const data = {
  name: document.getElementById('c-name').value,
  email: document.getElementById('c-email').value,
  subject: document.getElementById('c-subject').value,
  message: document.getElementById('c-message').value
};
const msgEl = document.getElementById('contact-msg');
msgEl.innerText = 'Sending...';
fetch(CONTACT_FUNCTION_URL, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(data)
})
.then(res => res.json())
.then(result => { msgEl.innerText = '✓ ' + result.message; e.target.reset(); })
.catch(() => { msgEl.innerText = '✗ Error sending message. Check Cloud Function URL.'; });
return false;
}

// ===== CLOUD FUNCTION ORDER HANDLER =====
// Replace the URL below with your deployed Cloud Function Trigger URL
// e.g. https://asia-south1-elements-ecommerce.cloudfunctions.net/handle-order
const ORDER_FUNCTION_URL = 'https://handle-order-v3-927825491730.asia-south1.run.app';

document.getElementById('order-form').addEventListener('submit', function(e){
e.preventDefault();
const data = {
  name: document.getElementById('o-name').value,
  email: document.getElementById('o-email').value,
  product: document.getElementById('o-product').value
};
const msgEl = document.getElementById('order-msg');
msgEl.innerText = 'Placing order...';
fetch(ORDER_FUNCTION_URL, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(data)
})
.then(res => res.json())
.then(result => { msgEl.innerText = '✓ ' + result.message; e.target.reset(); })
.catch(() => { msgEl.innerText = '✗ Error placing order. Check Cloud Function URL.'; });
});
