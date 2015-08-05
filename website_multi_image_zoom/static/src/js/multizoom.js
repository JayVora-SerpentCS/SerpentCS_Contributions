
// Multi-Zoom Script (c)2012 John Davenport Scheuer
// as first seen in http://www.dynamicdrive.com/forums/
// username: jscheuer1 - This Notice Must Remain for Legal Use
// requires: a modified version of Dynamic Drive's Featured Image Zoomer (w/ adjustable power) (included)

/*Featured Image Zoomer (May 8th, 2010)
* This notice must stay intact for usage 
* Author: Dynamic Drive at http://www.dynamicdrive.com/
* Visit http://www.dynamicdrive.com/ for full source code
*/

// Feb 21st, 2011: Script updated to v1.5, which now includes new feature by jscheuer1 (http://www.dynamicdrive.com/forums/member.php?u=2033) to show optional "magnifying lens" while over thumbnail image.
// March 1st, 2011: Script updated to v1.51. Minor improvements to inner workings of script.
// July 9th, 12': Script updated to v1.5.1, which fixes mouse wheel issue with script when used with a more recent version of jQuery.
// Nov 5th, 2012: Unofficial update to v1.5.1m for integration with multi-zoom (adds multiple images to be zoomed via thumbnail activated image swapping)
// Nov 28th, 2012: Version 2.1 w/Multi Zoom, updates - new features and bug fixes

var featuredimagezoomer = { // the two options for Featured Image Zoomer:
	loadinggif: '/website_multi_image_zoom/static/src/img/spinningred.gif', // full path or URL to "loading" gif
	magnifycursor: 'crosshair' // value for CSS's 'cursor' property when over the zoomable image
};

	//////////////// No Need To Edit Beyond Here ////////////////

//jQuery.noConflict();

$(document).ready(function() {

	$('head').append('<style type="text/css">.featuredimagezoomerhidden {visibility: hidden!important;}</style>');

	$.fn.multizoomhide = function(){
		return $('<style type="text/css">' + this.selector + ' {visibility: hidden;}<\/style>').appendTo('head');
	};

	$.fn.addmultizoom = function(options){

		var indoptions = {largeimage: options.largeimage}, $imgObj = $(options.imgObj + ':not(".thumbs")'),
		$descArea = $(options.descArea), first = true, splitre = /, ?/;

		options = $.extend({
				speed: 'fast',
				initzoomablefade: true,
				zoomablefade: true
			}, options);

		function loadfunction(){
			var lnk = this, styleobj1 = {}, styleobj2 = {}, $nim, lnkd, lnkt, lnko, w, h;
			if((lnkd = lnk.getAttribute('data-dims'))){
				lnkd = lnkd.split(splitre);
				w = lnkd[0]; h = lnkd[1];
			}
			$(new Image()).error(function(){
				if(lnk.tagName && !options.notmulti){
					alert("Error: I couldn't find the image:\n\n" + lnk.href + ((lnkt = lnk.getAttribute('data-title'))? '\n\n"' + lnkt + '"' : ''));
					if((lnko = $imgObj.data('last-trigger'))){
						first = true;
						$(lnko).trigger('click');
					}
				}
			}).load(function(){
				var opacity = $imgObj.css('opacity'), combinedoptions = {}, $parent;
				if(isNaN(opacity)){opacity = 1;}
				if(options.notmulti || !indoptions.largeimage){
					w = options.width || $imgObj.width(); h = options.height || $imgObj.height();
				}
				$imgObj.attr('src', this.src).css({width: w || options.width || this.width, height: (h = +(h || options.height || this.height))});
				if($imgObj.data('added')) {$imgObj.data('added').remove()};
				$imgObj.data('last-trigger', lnk);
				if(options.imagevertcenter){styleobj1 = {top: ($imgObj.parent().innerHeight() - h) / 2};}
				$imgObj.css(styleobj1).addimagezoom($.extend(combinedoptions, options, indoptions))
					.data('added', $('.magnifyarea:last' + (combinedoptions.cursorshade? ', .cursorshade:last' : '') + ', .zoomstatus:last, .zoomtracker:last'));
				if(options.magvertcenter){
					$('.magnifyarea:last').css({marginTop: (h - $('.magnifyarea:last').height()) / 2});
				}
				if(options.descpos){
					$parent = $imgObj.parent();
					styleobj2 = {left: $parent.offset().left + ($parent.outerWidth() - $parent.width()) / 2, top: h + $imgObj.offset().top};
				}
				if(options.notmulti){
					$descArea.css(styleobj2);
				} else {
					$descArea.css(styleobj2).empty().append(lnk.getAttribute('data-title') || '');
				}
				if(+opacity < 1){$imgObj.add($descArea).animate({opacity: 1}, options.speed);}
			}).attr('src', $imgObj.data('src'));
		}

		this.click(function(e){
			e.preventDefault();
			var src = $imgObj.attr('src'), ms, zr, cs, opacityObj = {opacity: 0};
			if(!first && (src === this.href || src === this.getAttribute('href'))){return;}
			if(first && !options.initzoomablefade || !options.zoomablefade){opacityObj = {};}
			first = false;
			indoptions.largeimage = this.getAttribute('data-large') || options.largeimage || '';
			if(indoptions.largeimage === 'none'){indoptions.largeimage = '';}
			if((ms = this.getAttribute('data-magsize')) || options.magnifiersize){
				indoptions.magnifiersize = (ms? ms.split(splitre) : '') || options.magnifiersize;
			} else {delete indoptions.magnifiersize;}
			indoptions.zoomrange = ((zr = this.getAttribute('data-zoomrange'))? (zr = zr.split(splitre)) : '') || options.zoomrange || '';
			if(zr){zr[0] = +zr[0]; zr[1] = +zr[1];}
			indoptions.cursorshade = ((cs = this.getAttribute('data-lens'))? cs : '') || options.cursorshade || '';
			if(cs){indoptions.cursorshade = eval(cs);}
			$imgObj.data('added') &&
				$imgObj.stop(true, true).data('added').not('.zoomtracker').remove().end()
					.css({background: 'url(' + featuredimagezoomer.loadinggif + ') center no-repeat'});
			$imgObj.css($.extend({visibility: 'visible'}, ($imgObj.data('added')? options.zoomablefade? {opacity: 0.25} : opacityObj : opacityObj))).data('src', this.href);
			$descArea.css($.extend({visibility: 'visible'}, opacityObj));
			loadfunction.call(this);
		}).eq(0).trigger('click');

		return this;
	};

	// Featured Image Zoomer main code:

	$.extend(featuredimagezoomer, {

		dsetting: { //default settings
				magnifierpos: 'right',
				magnifiersize:[200, 200],
				cursorshadecolor: '#fff',
				cursorshadeopacity: 0.3,
				cursorshadeborder: '1px solid black',
				cursorshade: false,
				leftoffset: 15, //offsets here are used (added to) the width of the magnifyarea when
				rightoffset: 10 //calculating space requirements and to position it visa vis any drop shadow
			},

		isie: (function(){/*@cc_on @*//*@if(@_jscript_version >= 5)return true;@end @*/return false;})(), //is this IE?

		showimage: function($tracker, $mag, showstatus){
			var specs=$tracker.data('specs'), d=specs.magpos, fiz=this;
			var coords=$tracker.data('specs').coords //get coords of tracker (from upper corner of document)
			specs.windimensions={w:$(window).width(), h:$(window).height()}; //remember window dimensions
			var magcoords={} //object to store coords magnifier DIV should move to
			magcoords.left = coords.left + (d === 'left'? -specs.magsize.w - specs.lo : $tracker.width() + specs.ro);
			//switch sides for magnifiers that don't have enough room to display on the right if there's room on the left:
			if(d!=='left' && magcoords.left + specs.magsize.w + specs.lo >= specs.windimensions.w && coords.left - specs.magsize.w >= specs.lo){
				magcoords.left = coords.left - specs.magsize.w - specs.lo;
			} else if(d==='left' && magcoords.left < specs.ro) { //if there's no room on the left, move to the right
				magcoords.left = coords.left + $tracker.width() + specs.ro;
			}
			$mag.css({left: magcoords.left, top:coords.top}).show(); //position magnifier DIV on page
			specs.$statusdiv.html('Current Zoom: '+specs.curpower+'<div style="font-size:80%">Use Mouse Wheel to Zoom In/Out</div>');
			if (showstatus) //show status DIV? (only when a range of zoom is defined)
				fiz.showstatusdiv(specs, 400, 2000);
		},

		hideimage: function($tracker, $mag, showstatus){
			var specs=$tracker.data('specs');
			$mag.hide();
			if (showstatus)
				this.hidestatusdiv(specs);
		},

		showstatusdiv: function(specs, fadedur, showdur){
			clearTimeout(specs.statustimer)
			specs.$statusdiv.css({visibility: 'visible'}).fadeIn(fadedur) //show status div
			specs.statustimer=setTimeout(function(){featuredimagezoomer.hidestatusdiv(specs)}, showdur) //hide status div after delay
		},

		hidestatusdiv: function(specs){
			specs.$statusdiv.stop(true, true).hide()
		},

		getboundary: function(b, val, specs){ //function to set x and y boundaries magnified image can move to (moved outside moveimage for efficiency)
			if (b=="left"){
				var rb=-specs.imagesize.w*specs.curpower+specs.magsize.w
				return (val>0)? 0 : (val<rb)? rb : val
			}
			else{
				var tb=-specs.imagesize.h*specs.curpower+specs.magsize.h
				return (val>0)? 0 : (val<tb)? tb : val
			}
		},

		moveimage: function($tracker, $maginner, $cursorshade, e){
			var specs=$tracker.data('specs'), csw = Math.round(specs.magsize.w/specs.curpower), csh = Math.round(specs.magsize.h/specs.curpower),
			csb = specs.csborder, fiz = this, imgcoords=specs.coords, pagex=(e.pageX || specs.lastpagex), pagey=(e.pageY || specs.lastpagey),
			x=pagex-imgcoords.left, y=pagey-imgcoords.top;
			$cursorshade.css({ // keep shaded area sized and positioned proportionately to area being magnified
				visibility: '',
				width: csw,
				height: csh,
				top: Math.min(specs.imagesize.h-csh-csb, Math.max(0, y-(csb+csh)/2)) + imgcoords.top,
				left: Math.min(specs.imagesize.w-csw-csb, Math.max(0, x-(csb+csw)/2)) + imgcoords.left
			});
			var newx=-x*specs.curpower+specs.magsize.w/2 //calculate x coord to move enlarged image
			var newy=-y*specs.curpower+specs.magsize.h/2
			$maginner.css({left:fiz.getboundary('left', newx, specs), top:fiz.getboundary('top', newy, specs)})
			specs.$statusdiv.css({left:pagex-10, top:pagey+20})
			specs.lastpagex=pagex //cache last pagex value (either e.pageX or lastpagex), as FF1.5 returns undefined for e.pageX for "DOMMouseScroll" event
			specs.lastpagey=pagey
		},

		magnifyimage: function($tracker, e, zoomrange){
			if (!e.detail && !e.wheelDelta){e = e.originalEvent;}
			var delta=e.detail? e.detail*(-120) : e.wheelDelta //delta returns +120 when wheel is scrolled up, -120 when scrolled down
			var zoomdir=(delta<=-120)? "out" : "in"
			var specs=$tracker.data('specs')
			var magnifier=specs.magnifier, od=specs.imagesize, power=specs.curpower
			var newpower=(zoomdir=="in")? Math.min(power+1, zoomrange[1]) : Math.max(power-1, zoomrange[0]) //get new power
			var nd=[od.w*newpower, od.h*newpower] //calculate dimensions of new enlarged image within magnifier
			magnifier.$image.css({width:nd[0], height:nd[1]})
			specs.curpower=newpower //set current power to new power after magnification
			specs.$statusdiv.html('Current Zoom: '+specs.curpower)
			this.showstatusdiv(specs, 0, 500)
			$tracker.trigger('mousemove')
		},

		highestzindex: function($img){
			var z = 0, $els = $img.parents().add($img), elz;
			$els.each(function(){
				elz = $(this).css('zIndex');
				elz = isNaN(elz)? 0 : +elz;
				z = Math.max(z, elz);
			});
			return z;
		},

		init: function($img, options){
			var setting=$.extend({}, this.dsetting, options), w = $img.width(), h = $img.height(), o = $img.offset(),
			fiz = this, $tracker, $cursorshade, $statusdiv, $magnifier, lastpage = {pageX: 0, pageY: 0},
			basezindex = setting.zIndex || this.highestzindex($img);
			if(h === 0 || w === 0){
				$(new Image()).load(function(){
					featuredimagezoomer.init($img, options);
				}).attr('src', $img.attr('src'));
				return;
			}
			$img.css({visibility: 'visible'});
			setting.largeimage = setting.largeimage || $img.get(0).src;
			$magnifier=$('<div class="magnifyarea" style="position:absolute;z-index:2;width:'+setting.magnifiersize[0]+'px;height:'+setting.magnifiersize[1]+'px;left:-10000px;top:-10000px;visibility:hidden;overflow:hidden;border:1px solid black;" />')
				.append('<div style="position:relative;left:0;top:0;z-index:'+basezindex+';" />')
				.appendTo(document.body) //create magnifier container
			//following lines - create featured image zoomer divs, and absolutely positioned them for placement over the thumbnail and each other:
			if(setting.cursorshade){
				$cursorshade = $('<div class="cursorshade" style="visibility:hidden;position:absolute;left:0;top:0;z-index:'+basezindex+';" />')
					.css({border: setting.cursorshadeborder, opacity: setting.cursorshadeopacity, backgroundColor: setting.cursorshadecolor})
					.appendTo(document.body);
			} else { 
				$cursorshade = $('<div />'); //dummy shade div to satisfy $tracker.data('specs')
			}
			$statusdiv = $('<div class="zoomstatus preloadevt" style="position:absolute;visibility:hidden;left:0;top:0;z-index:'+basezindex+';" />')
				.html('<img src="'+this.loadinggif+'" />')
				.appendTo(document.body); //create DIV to show "loading" gif/ "Current Zoom" info
			$tracker = $('<div class="zoomtracker" style="cursor:progress;position:absolute;z-index:'+basezindex+';left:'+o.left+'px;top:'+o.top+'px;height:'+h+'px;width:'+w+'px;" />')
				.css({backgroundImage: (this.isie? 'url(cannotbe)' : 'none')})
				.appendTo(document.body);
			$(window).bind('load resize', function(){ //in case resizing the window repostions the image or description
					var o = $img.offset(), $parent;
					$tracker.css({left: o.left, top: o.top});
					if(options.descpos && options.descArea){
						$parent = $img.parent();
						$(options.descArea).css({left: $parent.offset().left + ($parent.outerWidth() - $parent.width()) / 2, top: $img.height() + o.top});
					}
				});

			function getspecs($maginner, $bigimage){ //get specs function
				var magsize={w:$magnifier.width(), h:$magnifier.height()}
				var imagesize={w:w, h:h}
				var power=(setting.zoomrange)? setting.zoomrange[0] : ($bigimage.width()/w).toFixed(5)
				$tracker.data('specs', {
					$statusdiv: $statusdiv,
					statustimer: null,
					magnifier: {$outer:$magnifier, $inner:$maginner, $image:$bigimage},
					magsize: magsize,
					magpos: setting.magnifierpos,
					imagesize: imagesize,
					curpower: power,
					coords: getcoords(),
					csborder: $cursorshade.outerWidth(),
					lo: setting.leftoffset,
					ro: setting.rightoffset
				})
			}

			function getcoords(){ //get coords of thumb image function
				var offset=$tracker.offset() //get image's tracker div's offset from document
				return {left:offset.left, top:offset.top}
			}

			$tracker.mouseover(function(e){
						$cursorshade.add($magnifier).add($statusdiv).removeClass('featuredimagezoomerhidden');
						$tracker.data('premouseout', false);
				}).mouseout(function(e){
						$cursorshade.add($magnifier).add($statusdiv.not('.preloadevt')).addClass('featuredimagezoomerhidden');
						$tracker.data('premouseout', true);
				}).mousemove(function(e){ //save tracker mouse position for initial magnifier appearance, if needed
					lastpage.pageX = e.pageX;
					lastpage.pageY = e.pageY;
				});

			$tracker.one('mouseover', function(e){
				var $maginner=$magnifier.find('div:eq(0)')
				var $bigimage=$('<img src="'+setting.largeimage+'"/>').appendTo($maginner)
				var largeloaded = featuredimagezoomer.loaded[$('<a href="'+setting.largeimage+'"></a>').get(0).href];
				var showstatus=setting.zoomrange && setting.zoomrange[1]>setting.zoomrange[0]
				var imgcoords=getcoords()
				if(!largeloaded){
					$img.stop(true, true).css({opacity:0.1}) //"dim" image while large image is loading
					$statusdiv.css({left:imgcoords.left+w/2-$statusdiv.width()/2, top:imgcoords.top+h/2-$statusdiv.height()/2, visibility:'visible'})
				}
				$bigimage.bind('loadevt', function(event, e){ //magnified image ONLOAD event function (to be triggered later)
					if(e.type === 'error'){
						$img.css({opacity: 1}).data('added').remove();
						var src = $('<a href="' + $bigimage.attr('src') + '"></a>').get(0).href;
						if(window.console && console.error){
							console.error('Cannot find Featured Image Zoomer larger image: ' + src);
						} else {
							alert('Cannot find Featured Image Zoomer larger image:\n\n' + src);
						}
						return;
					}
					featuredimagezoomer.loaded[this.src] = true;
					$img.css({opacity:1}) //restore thumb image opacity
					$statusdiv.empty().css({border:'1px solid black', background:'#C0C0C0', padding:'4px', font:'bold 13px Arial', opacity:0.8}).hide().removeClass('preloadevt');
					if($tracker.data('premouseout')){
						$statusdiv.addClass('featuredimagezoomerhidden');
					}
					if (setting.zoomrange){ //if set large image to a specific power
						var nd=[w*setting.zoomrange[0], h*setting.zoomrange[0]] //calculate dimensions of new enlarged image
						$bigimage.css({width:nd[0], height:nd[1]})
					}
					getspecs($maginner, $bigimage) //remember various info about thumbnail and magnifier
					$magnifier.css({display:'none', visibility:'visible'})
					$tracker.mouseover(function(e){ //image onmouseover
						$tracker.data('specs').coords=getcoords() //refresh image coords (from upper left edge of document)
						fiz.showimage($tracker, $magnifier, showstatus)
					})
					$tracker.mousemove(function(e){ //image onmousemove
						fiz.moveimage($tracker, $maginner, $cursorshade, e)
					})
					if (!$tracker.data('premouseout')){
						fiz.showimage($tracker, $magnifier, showstatus);
						fiz.moveimage($tracker, $maginner, $cursorshade, lastpage);
					}
					$tracker.mouseout(function(e){ //image onmouseout
						fiz.hideimage($tracker, $magnifier, showstatus)
					}).css({cursor: fiz.magnifycursor});
					if (setting.zoomrange && setting.zoomrange[1]>setting.zoomrange[0]){ //if zoom range enabled
						$tracker.bind('DOMMouseScroll mousewheel', function(e){
							fiz.magnifyimage($tracker, e, setting.zoomrange);
							e.preventDefault();
						});
					} else if(setting.disablewheel){
						$tracker.bind('DOMMouseScroll mousewheel', function(e){e.preventDefault();});
					}
				})	//end $bigimage onload
				if ($bigimage.get(0).complete){ //if image has already loaded (account for IE, Opera not firing onload event if so)
					$bigimage.trigger('loadevt', {type: 'load'})
				}
				else{
					$bigimage.bind('load error', function(e){$bigimage.trigger('loadevt', e)})
				}
			})
		},

		iname: (function(){var itag = $('<img />'), iname = itag.get(0).tagName; itag.remove(); return iname;})(),

		loaded: {},

		hashre: /^#/
	});

	$.fn.addimagezoom = function(options){
		var sel = this.selector, $thumbs = $(sel.replace(featuredimagezoomer.hashre, '.') + '.thumbs a');
		options = options || {};
		if(options.multizoom !== null && ($thumbs).size()){
			$thumbs.addmultizoom($.extend(options, {imgObj: sel, multizoom: null}));
			return this;
		} else if(options.multizoom){
			$(options.multizoom).addmultizoom($.extend(options, {imgObj: sel, multizoom: null}));
			return this;
		} else if (options.multizoom !== null){
			return this.each(function(){
				if (this.tagName !== featuredimagezoomer.iname)
					return true; //skip to next matched element
				$('<a href="' + this.src + '"></a>').addmultizoom($.extend(options, {imgObj: sel, multizoom: null, notmulti: true}));
			});
		}
		return this.each(function(){ //return jQuery obj
			if (this.tagName !== featuredimagezoomer.iname)
				return true; //skip to next matched element
			featuredimagezoomer.init($(this), options);
		});
	};

});
