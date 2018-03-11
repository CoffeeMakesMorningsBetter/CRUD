$(function() {
  $("#bootcamp").on("click", "i", function(event) {
    event.preventDefault();
    let id = $(this)
      .closest("li")
      .attr("id");
    $.ajax({
      method: "DELETE",
      url: `/bootcamps/${id}`
    }).then(
      data => {
        $(this)
          .closest("li")
          .hide();
      },
      function() {
        console.log("Something is Wrong");
      }
    );
  });
  $("#bootcamp").on("click", "button", function(event) {
    let direction = $(event.target).attr("class");
    event.preventDefault();
    let id = $(this)
      .closest("li")
      .attr("id");
    let num = $(this)
      .next()
      .next("span")
      .text();
    $.ajax({
      method: "PATCH",
      url: `/bootcamps/${id}/vote`,
      data: { votes: direction }
    }).then(
      data => {
        $(event.target)
          .siblings("span")
          .text(data.votes);
        // get sorted list
        let $ul = $("ul");
        let store = $("li").sort(function(a, b) {
          let aup = parseInt(
            $(a)
              .find("span")
              .text()
          );
          let bup = parseInt(
            $(b)
              .find("span")
              .text()
          );
          if (aup < bup) {
            return 1;
          }
          if (bup > aup) {
            return -1;
          }
          return 0;
        });
        // empty ul
        store.detach().appendTo($ul);
      },
      function() {
        console.log("Something is Wrong");
      }
    );
  });
});
