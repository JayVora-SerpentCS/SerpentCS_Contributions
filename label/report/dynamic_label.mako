<html>
    <style type="text/css">
        body {
            height: 297mm;
            width: 210mm;
            /* to centre page on screen*/
            margin-left: auto;
            margin-right: auto;
            margin-top:auto;
            margin-bottom:auto;
            font-family:Verdana; 
            font-size:11pt;
        }
        .rotate {
            -moz-transform: rotate(90.0deg);  /* FF3.5+ */
            -o-transform: rotate(90.0deg);  /* Opera 10.5 */
            -webkit-transform: rotate(90.0deg);  /* Saf3.1+, Chrome */
             filter:  progid:DXImageTransform.Microsoft.BasicImage(rotation=0.083);  /* IE6,IE7 */
            -ms-filter: "progid:DXImageTransform.Microsoft.BasicImage(rotation=0.083)"; /* IE8 */
        }
        table {
            border-top-color: lightgray;
            border-bottom-color: lightgray;
            border-right-color: lightgray;
            border-left-color: lightgray;
        }
    </style>
    <body>
        <% row_no=1 %>
        <div style="display: table; height: 297mm;width: 210mm; #position: relative; overflow: hidden;" >
        <div style=" #position: absolute; #top: 50%;display: table-cell; vertical-align: middle;">
        <div style="#position: relative; #top: -50%; ">
        <table cellspacing="${datas.get('cell_spacing')}" align="center" >
        %for row in get_record(datas.get('rows'), datas.get('columns'), datas.get('ids'), datas.get('model'), datas.get('number_of_copy')):
               <tr height=${datas.get('height')}>
                    %for col in row:
                        <td width=${datas.get('width')} style="padding: ${datas.get('top_margin')}mm ${datas.get('right_margin')}mm ${datas.get('bottom_margin')}mm ${datas.get('left_margin')}mm">
                            <div class="rotate">
                            %for val in col:
                                %if val.get('newline'):
                                    <br/>
                                %endif
                                <div style="${val.get('style')}" />
                                    %if val.get('type') == 'normal':
                                        ${val.get('string')}${val.get('value')}
                                    %elif val.get('type') == 'image':
                                        ${val.get('string')}${helper.embed_image('png', val.get('value'), datas.get('image_width', 50),datas.get('image_height', 50))|n}
                                    %elif val.get('type') == 'barcode':
                                        ${val.get('string')}${helper.embed_image('png', generate_barcode(val.get('value'),datas.get('barcode_width', 50),datas.get('barcode_height', 50)), datas.get('barcode_width', 50), datas.get('barcode_height', 50))|n}
                                    %endif
                                </div>
                            %endfor
                            </div>
                        </td>
                    %endfor
               </tr>
               %if row_no < ((datas.get('rows')+1)*datas.get('number_of_copy')) : 
                    %if (row_no % datas.get('no_row_per_page')) == 0 :
                        </table></div></div></div>
                        <div style="page-break-after: always;"><span style="display: none;">&nbsp;</span></div>
                        <div style="display: table; height: 297mm;width: 210mm; #position: relative; overflow: hidden;">
                        <div style=" #position: absolute; #top: 50%;display: table-cell; vertical-align: middle;">
                        <div style="#position: relative; #top: -50%; ">
                        <table cellspacing="${datas.get('cell_spacing')}" align="center">
                    %endif
               %endif
               <% row_no+=1 %>
        %endfor
        <% completed_row = (row_no-1) % datas.get('no_row_per_page') %>
        %if completed_row != 0 :
            %for remain in range(completed_row,datas.get('no_row_per_page')):
                <tr height=${datas.get('height')}>
                    %for col in range(datas.get('columns')):
                        <td width=${datas.get('width')} style="padding: ${datas.get('top_margin')}px ${datas.get('right_margin')}px ${datas.get('bottom_margin')}px ${datas.get('left_margin')}px">
                            &nbsp;
                        </td>
                    %endfor
                </tr>
            %endfor
        %endif
        </table></div></div></div>
    </body>
</html>