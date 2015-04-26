// TekMenu by comunicatek.com  under the mit license.
// Author:  Dani Prados
// http://code.comunicatek.com
(function($) {
 
   //
  // plugin defaults
  //
  var  defaults = {
    timeout: 250,
	fullAnimation : false,
	debug:false
  };
 
  //
  // plugin definition
  //
  
	$.fn.TekMenu = function(options) { 
	var opts;
	
	function debug2(str) {
		if (opts.debug && window.console && window.console.log){
		  window.console.log(str);
		}
	}	

	function debug($obj) {
	  debug2('menu: ' + $obj.size());
	}
	
	function oculta2(menu){
		var o = opts;
		var toca =	$(menu).data("toca");
		if(toca){
			debug2("oculta 2 (toca)"+$(menu).attr("id"));
			if(o.fullAnimation){
				$(menu).queue(function(next){
					  $(this).hide();
					  next();
					});
			} else {
				$(menu).stop(true,true).hide();
			}
		} else {
			debug2("oculta 2 (no toca)"+$(menu).attr("id"));
		}
	}

	function oculta(){
		//var o = $.fn.TekMenu.opts;
		var o = opts;
		var menu = $(this).attr("rel");
		var id = setTimeout(function(a){ return function(){ oculta2(a);}; }(menu),o.timeout);
		debug2("oculta "+$(this).attr("rel")+" "+id); 
		$(menu).data("idtimeout",id);
	}
	
	function mostra(){
		var menu = $(this).attr("rel");
		$(menu).data("toca",false);
		var o = opts;
		clearTimeout($(menu).data("idtimeout"));
		debug2("mostra   "+$(this).attr("rel")+" "+$(menu).data("idtimeout"));
		var position = $(this).position();
		var height = $(this).outerHeight();
		var x = position.left;
		var y = position.top+height+1;
		$(menu).css({left:x,top:y}).slideDown("slow");
		$(menu).unbind('mouseenter mouseleave');
		$(menu).data("toca",true);
		$(menu).hover(function(){ 
				debug2("reset timer   "+$(menu).attr("id")+" "+$(menu).data("idtimeout"));							   
				$(this).data("toca",false); 
				clearTimeout($(menu).data("idtimeout"));
			},
			function(){ 
				$(this).data("toca",true); 
				var id = setTimeout(function(a){ return function(){ oculta2(a);}; }(menu),o.timeout);
				debug2("timer oculta  "+$(menu).attr("id")+" "+id);
				$(this).data("idtimeout",id);
			}
		);
	}
	  
	// Main  code
	opts = $.extend({}, defaults, options);
    
	debug(this);
    // build main options before element iteration
    return this.hover(mostra ,oculta);
  };
//
// end of closure
//
})(jQuery);