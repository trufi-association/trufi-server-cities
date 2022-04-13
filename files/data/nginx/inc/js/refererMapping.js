function resolveBackendInterweb(r) {
	r.warn("EXTENSION RESOLVER FOR INTERWEB");
	let url = r.uri;
	let backendurl = "http://";
	
	let city = "";
	let extensionname = "";
	let extensionpath = "";
	
	if (url.endsWith("/")) {
		let urlsplitted = url.split("");
		urlsplitted[urlsplitted.length-1] = "";
		url = urlsplitted.join("");
	}
	
	let cityExtension = new RegExp("/(.+?)/(.+?)$", "i");
	if (cityExtension.test(url)) {
		city = url.replace(cityExtension, "$1"); // /(.+?)/(.+?)$ --> $1 e.g. '/germany-hamburg/opentripplanner/otp' --> 'germany-hamburg' or '/germany-hamburg/opentripplanner' --> 'germany-hamburg'
		let path = url.replace(cityExtension, "$2"); // /(.+?)/(.+?)$ --> $2 e.g. '/germany-hamburg/opentripplanner/otp' --> 'opentripplanner/otp' or '/germany-hamburg/opentripplanner' --> 'opentripplanner'
		if (path.includes("/")) { // e.g. "opentripplanner/otp".includes("/") == true then
			// it is not just the name of the extension itself but also contains the path to the resource the extension provides
			// e.g. 'opentripplanner/otp'
			let extensionPath = new RegExp("(.+?)/(.+?)$", "i");
			extensionname = path.replace(extensionPath, "$1"); // e.g. 'opentripplanner/otp' --> 'opentripplanner'
			extensionpath = path.replace(extensionPath, "$2"); // e.g. 'opentripplanner/otp' --> 'otp'
		} else {
			extensionname = path;
		}
	}
	
	backendurl += extensionname + "_" + city + "/" + extensionpath
	r.warn("Internal resolvement: " + url + " --> " + backendurl)
	return backendurl
	
}

function resolveBackendIntraweb(r) {
	r.warn("EXTENSION RESOLVER FOR INTRAWEB");
	let referer = r.headersIn.referer;
	if (referer == undefined) {
		return resolveBackendInterweb(r);
	} else {
		// extract city prefix, name of extension and extension url path
		let re = new RegExp("http://(.+?)/(.+?)/(.+?)$", "i");
		let city = referer.replace(re, "$2");
		let path = referer.replace(re, "$3");
		let extensionname = path.split("/")[0]
		
		// fix uri
		let url = r.uri;
		re = new RegExp("/(.+?)/(.+?)$", "i");
		let path1 = url.replace(re, "$1");
		if (path1 == city) {
			url = url.replace(re, "$2");
		}
		
		let backendurl = "http://" + extensionname + "_" + city + "/" + url
		r.warn("Internal resolvement based on referer: " + r.uri + " --> " + backendurl)
		return backendurl
		
	}
}

export default {resolveBackendInterweb, resolveBackendIntraweb}; 
