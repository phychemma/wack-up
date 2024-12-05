let all_posts=document.querySelectorAll('.post')
for(let post of all_posts){
  post.addEventListener('click' , e=>{
    e.remove()
  })
}