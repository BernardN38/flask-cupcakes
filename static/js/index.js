const BaseUrl ='http://127.0.0.1:5000/api/cupcakes'



async function getCupcakes(){
    $('#main-cont').empty()
    let res = await axios.get(BaseUrl)
    for (let obj of res.data.cupcakes){
        $('#main-cont').append(`<div class='text-center'>${obj.flavor}</div>`)
    }
    console.log('got cupcakes ')
}

async function newCupcake(e){
    e.preventDefault()
    let cupcake = {}
    cupcake.flavor = $('#flavor').val()
    cupcake.size = $('#size').val()
    cupcake.rating = $('#rating').val()
    cupcake.image = $('#image').val()
    // cupcake = JSON.stringify(cupcake)
    console.log(cupcake)
    const res = await axios.post(BaseUrl, cupcake)
    console.log(res)
    getCupcakes()
}




$('#submit').click(newCupcake)

getCupcakes()