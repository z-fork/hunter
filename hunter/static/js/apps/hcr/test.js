//配置
var config = {
  'audio':{
    'icon':'audio-record-play',
    'text':true
  },
  'loading': 'loading-ic'
};

//loading
window.onload = function(){
  $('#loading').hide()
};

//分享
$('#js-btn-share').bind('tap',function(){
  $('#js-share').show()
});
$('#js-share').bind('tap',function(){
  $(this).hide()
});


var pageIndex = 1,
	pageTotal = $('.page').length,
	TOWARDS = {
        up: 1,
        right: 2,
        down: 3,
        left: 4
    },
	isAnimating = false;

//禁用手机默认的触屏滚动行为
document.addEventListener('touchmove', function(e) {
	e.preventDefault();
}, false);

$(document).swipeLeft(function() {
    console.log('swipe left...');
	if (isAnimating) return;
	if (pageIndex < pageTotal) {
		pageIndex += 1;
	}else{
		pageIndex = 1;
	}
	pageMove(TOWARDS.up);
});

$(document).swipeRight(function(){
	if (isAnimating) return;
	if (pageIndex > 1) {
		pageIndex-=1
	} else {
		pageIndex=pageTotal
	}
	pageMove(TOWARDS.down)
});

function pageMove(tw) {
	var lastPage,
        outClass,
        inClass;

	if(tw == TOWARDS.left) {
		if(pageIndex == 1) {
			lastPage = ".page-" + pageTotal;
		} else {
			lastPage = ".page-" + (pageIndex - 1);
		}
	} else if(tw == TOWARDS.right) {
		if(pageIndex == pageTotal) {
			lastPage = ".page-1";
		} else {
			lastPage = ".page-" + (pageIndex + 1);
		}
	}

	var nowPage = ".page-" + pageIndex;

	switch(tw) {
		case TOWARDS.left:
			outClass = 'pt-page-moveToTop';
			inClass = 'pt-page-moveFromBottom';
			break;
		case TOWARDS.right:
			outClass = 'pt-page-moveToBottom';
			inClass = 'pt-page-moveFromTop';
			break;
	}

	isAnimating = true;
	$(nowPage).removeClass("hide");

	$(lastPage).addClass(outClass);
	$(nowPage).addClass(inClass);

	setTimeout(function() {
		$(lastPage).removeClass('page-current');
		$(lastPage).removeClass(outClass);
		$(lastPage).addClass("hide");
		$(lastPage).find("img").addClass("hide");

		$(nowPage).addClass('page-current');
		$(nowPage).removeClass(inClass);
		$(nowPage).find("img").removeClass("hide");

		isAnimating = false;
	}, 600);
}
