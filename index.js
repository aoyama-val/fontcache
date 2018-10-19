const AWS = require("aws-sdk");
const fs = require("fs");
const pdf = require("html-pdf");

const BUCKET_NAME = "バケット名を入れてね";

exports.handler = (event, context, callback) => {
  console.log("Hello");

  var options = {
    format: "A4",        // allowed units: A3, A4, A5, Legal, Letter, Tabloid
    orientation: "portrait", // portrait or landscape
  };

  //process.env.FONTCONFIG_PATH = "/var/task/fonts";

  var html = '<div style="">mogemoge あいうえお Hello</div>';
  var pdfFileName = "/tmp/hoge.pdf";

  console.log("cwd", process.cwd());

  pdf.create(html, options).toFile(pdfFileName, function(err, res) {
    if (err) {
      context.fail("Hello");
    } else {
        AWS.config.update({ region: "ap-northeast-1" });
        var s3 = new AWS.S3();
        var key = new Date().getTime() + ".pdf";
        var content = fs.readFileSync(pdfFileName);
        var params = {
            Bucket: BUCKET_NAME,
            Key: key,
            Body: content,
        };
        s3.putObject(params).promise()
        .then(function() {
          context.succeed("Hello");
        });
    }
  });

};
