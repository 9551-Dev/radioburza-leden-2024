var current_image_index = 0;
var image_paths = [
    {{image_paths}}
];

function open_image_viewer(image_path) {
    current_image_index = image_paths.indexOf(image_path);
    update_image_viewer();
    document.querySelector('.image-viewer').style.display = 'flex';
    document.body.style.overflow = 'hidden';

    document.addEventListener('keydown', handle_keypress);

    // Add event listener for mouse wheel
    document.querySelector('.gallery').addEventListener('wheel', function(event) {
        if (event.deltaY < 0) {
            // Scrolling up
            navigate_image(event, -1);
        } else {
            // Scrolling down
            navigate_image(event, 1);
        }
    });
}

function close_image_viewer() {
    var img = document.getElementById('viewer-image');
    img.style.transform = 'scale(1)';
    document.querySelector('.image-viewer').style.display = 'none';
    document.body.style.overflow = 'auto';

    document.removeEventListener('keydown', handle_keypress);
    document.querySelector('.gallery').removeEventListener('wheel', handle_wheel);
}

function navigate_image(event, direction) {
    var img = document.getElementById('viewer-image');
    img.style.transform = 'scale(1)';
    event.stopPropagation();
    current_image_index += direction;
    if (current_image_index < 0) {
        current_image_index = image_paths.length - 1;
    } else if (current_image_index >= image_paths.length) {
        current_image_index = 0;
    }
    update_image_viewer();
}

function update_image_viewer() {
    document.getElementById('viewer-image').src = image_paths[current_image_index];
}

function toggle_dark_mode() {
    var body = document.body;
    body.classList.toggle('dark-mode');
}

function zoom_image(event) {
    var img = document.getElementById('viewer-image');
    var bounding_rect = img.getBoundingClientRect();

    var x = (event.clientX - bounding_rect.left) / bounding_rect.width;
    var y = (event.clientY - bounding_rect.top) / bounding_rect.height;

    img.style.transformOrigin = `${x * 100}% ${y * 100}%`;
    img.style.transform = img.style.transform === 'scale(2)' ? 'scale(1)' : 'scale(2)';

    event.stopPropagation();
}

function handle_keypress(event) {
    if (document.querySelector('.image-viewer').style.display === 'flex') {
        switch(event.key) {
            case 'ArrowLeft':
                navigate_image(event, -1);
                break;
            case 'ArrowRight':
                navigate_image(event, 1);
                break;
            case 'Escape':
                close_image_viewer();
                break;
        }
    }
}

window.addEventListener('scroll', function () {
    var body = document.body;
    var scroll_position = window.scrollY;

    if (scroll_position > 0) {
        body.classList.add('scrolled');
    } else {
        body.classList.remove('scrolled');
    }
});
