uploading_area = document.querySelector('#upload-area');

video_upload_form = document.querySelector("#vid-upload-form");
image_upload_form = document.querySelector("#img-upload-form");
text_upload_form = document.querySelector("#text-upload-form");

function vidbtnclick(){
    uploading_area.classList.remove('hidden');

    video_upload_form.classList.remove('hidden');
    image_upload_form.classList.add('hidden');
    text_upload_form.classList.add('hidden');
}
function imgbtnclick(){
    uploading_area.classList.remove('hidden');

    video_upload_form.classList.add('hidden');
    image_upload_form.classList.remove('hidden');
    text_upload_form.classList.add('hidden');
}
function textbtnclick(){
    uploading_area.classList.remove('hidden');

    video_upload_form.classList.add('hidden');
    image_upload_form.classList.add('hidden');
    text_upload_form.classList.remove('hidden');
}

function addOrRemoveLike(post_id){
    thumb = document.getElementById('thumbs_'+post_id);
    local_likes =document.getElementById("postlikes_"+post_id);
    if (thumb.classList.contains('bi-hand-thumbs-up')){
        //to be liked
        console.log('liked')
        thumb.classList.remove('bi-hand-thumbs-up');
        thumb.classList.add('bi-hand-thumbs-up-fill');

        $.ajax({
            type: "GET",
            url: "/like_post",
            data:{
                postid:post_id,
            },
            success: function(data){
                console.log(data);
            }
        });

        //finally
        local_likes.innerText = parseInt(local_likes.innerText) + 1;
    }
    else if (thumb.classList.contains('bi-hand-thumbs-up-fill')){
        //to be removed from liked
        console.log('Like removed');
        thumb.classList.add('bi-hand-thumbs-up');
        thumb.classList.remove('bi-hand-thumbs-up-fill');

        $.ajax({
            type: "GET",
            url: "/remove_like",
            data:{
                postid:post_id,
            },
            success: function(data){
                console.log(data);
            }
        });


        //finally
        local_likes.innerText = parseInt(local_likes.innerText) - 1;
    }
}

function showComments(post_id){
    section = document.getElementById('comments-for-post-'+post_id);
    section.textContent = "";
    
    $.ajax({
        type: "GET",
        url: "/showcomments",
        data:{
            postid:post_id,
        },
        success: function(data){
            data.forEach(element => {
                // console.log(element.name, element.comment);
                // creating  a comment
                div = document.createElement('div')
                comment = document.createElement('span');
                comment.classList.add('single-comment-style');

                commenter = document.createElement('h6');
                commentbody = document.createElement('p');

                commenter.innerHTML  = "<i class='bi bi-person-circle'> </i>"+element.name;
                commentbody.innerText = element.comment;

                comment.appendChild(commenter);
                comment.appendChild(commentbody);

                div.appendChild(comment);
                //upload comment
                section.appendChild(div);
            });
        }
    });
    console.log('All comments Retrieved');

}

function uploadComment(post_id, fname, lname){
    section = document.getElementById('comments-for-post-'+post_id);

    data = document.getElementById('comment-field-'+post_id).value;
    if(data == ""){
        return;
    }
    //uploading the comment
    $.ajax({
        type: "GET",
        url: "/addcomment",
        data:{
            postid:post_id,
            commentdata:data,
        },
        success: function(data){
            console.log(data);
        }
        
    });
    // creating  a comment
    div = document.createElement('div')
    comment = document.createElement('span');
    comment.classList.add('single-comment-style');

    commenter = document.createElement('h6');
    commentbody = document.createElement('p');

    commenter.innerHTML  = "<i class='bi bi-person-circle'> </i>"+fname+ " "+lname;
    commentbody.innerText = data;

    comment.appendChild(commenter);
    comment.appendChild(commentbody);

    div.appendChild(comment);
    //upload comment
    section.appendChild(div);
    
    // console.log('clicked');
    document.getElementById('comment-field-'+post_id).value = "";
}


function followHandler(person_id){
    button =  document.querySelector('#follow-person-'+person_id);
    console.log(button.innerText, person_id);
    if(button.innerText === 'Follow'){
        $.ajax({
            type: "GET",
            url: "/follow",
            data:{
                id:person_id,
            },
            success: function(data){
                console.log(data);
                button.innerText = 'Unfollow';

            }
            
        });
    }
    if(button.innerText === 'Unfollow'){
        $.ajax({
            type: "GET",
            url: "/unfollow",
            data:{
                id:person_id,
            },
            success: function(data){
                console.log(data);
                button.innerText = 'Follow';
            }
            
        });
    }

}
