// Video page: the tour starts in place; a tutorial opens in the lightbox and plays; the lightbox closes when the video ends,
// with Escape, the close button or a click beside the video. Without JavaScript the link opens the MP4.
(function () {
  // The tour: only its picture and a play button until it is started, like the tutorials.
  document.querySelectorAll(".featured-player").forEach(function (player) {
    const video = player.querySelector("video");
    const button = player.querySelector(".play");
    video.controls = false;
    button.hidden = false;
    button.addEventListener("click", function () {
      button.remove();
      video.controls = true;
      video.focus();
      video.play().catch(function () {});
    });
  });

  const box = document.querySelector(".lightbox");
  if (!box || typeof box.showModal !== "function") return;
  const video = box.querySelector("video");
  let opener = null;

  function source(src, type) {
    const element = document.createElement("source");
    element.src = src;
    element.type = type;
    return element;
  }

  function track(src, lang, label) {
    const element = document.createElement("track");
    Object.assign(element, { kind: "subtitles", src: src, srclang: lang, label: label });
    return element;
  }

  document.querySelectorAll("a.video-thumb").forEach(function (link) {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      opener = link;
      const url = link.dataset.video;
      video.replaceChildren(source(url + ".webm", "video/webm"), source(url + ".mp4", "video/mp4"));
      if (link.dataset.subtitles) {
        video.append(track(url + ".en.vtt", "en", "English"), track(url + ".de.vtt", "de", "Deutsch"));
      }
      video.poster = url + ".jpg";
      box.setAttribute("aria-label", link.dataset.title || "Video");
      video.load();
      box.showModal();
      video.focus();
      video.play().catch(function () {});  // the player's own button still works if autoplay is refused
    });
  });

  video.addEventListener("ended", function () { box.close(); });
  box.querySelector(".lightbox-close").addEventListener("click", function () { box.close(); });
  box.addEventListener("click", function (event) { if (event.target === box) box.close(); });
  box.addEventListener("close", function () {
    video.pause();
    video.replaceChildren();
    video.removeAttribute("src");
    video.removeAttribute("poster");
    video.load();
    if (opener) opener.focus();
  });
})();
