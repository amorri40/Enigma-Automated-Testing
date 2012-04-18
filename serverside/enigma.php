<html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">

      // Load the Visualization API
      google.load('visualization', '1.0', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(drawVisualization);

      function drawVisualization() {
      // Create and populate the data table.
      var data = google.visualization.arrayToDataTable([
<?php echo "
        ['x', 'MacOSX', 'Windows', 'Linux']";
        mysql_connect(localhost,"enigmagames","enigma");
        @mysql_select_db("enigmagames") or die( "Unable to select database");

        $query = "SELECT * FROM enigma_stats_with_unimplemented";
        $result=mysql_query($query);
        $num=mysql_numrows($result);

        mysql_close();
        $i=0;
        while ($i < $num) {

        $x=mysql_result($result,$i,"x");
        $MacOSX=mysql_result($result,$i,"MACOSX");
        $WINDOWS=mysql_result($result,$i,"WINDOWS");
        $LINUX=mysql_result($result,$i,"LINUX");
        echo ",['$x' , $MacOSX , $WINDOWS , $LINUX ]";
        $i++;
        }
         ?>
      ]);

      // Create and draw the visualization.
      new google.visualization.LineChart(document.getElementById('visualization')).
          draw(data, {curveType: "line",
                      width: 1000, height: 400,
                      vAxis: {maxValue: 90, minValue:0}}
              );
    }
    </script>
  </head>

  <body>
    <div id="visualization"></div>
  </body>
</html>