#define scr_record_event
global.start_time=current_time
//argument0=event name
//the_event_type=argument0
the_event_number=argument1
write_whole_room=argument2 //wheterh to write all the instance data on this event

event_shortname=argument0
nl = "
"
if event_shortname=="bs" {
room_data=scr_write_roomdata();
event_shortname=string(global.framenumber)+": beginStep:"+room_data;
} else if write_whole_room==true {
   room_data=scr_write_roomdata();
   event_shortname+=":"+room_data
   ds_queue_enqueue(global.events,","+event_shortname);
   return 0;
}
ds_queue_enqueue(global.events,event_shortname);
#define scr_write_roomdata
room_data="["
data_sep=","
//globalvar previous,current;

global.write_called+=1

frame_data=ds_map_create();

for (i=0; i<instance_count; i+=1)
  {
    iii = instance_id[i];
    //if iii <100000 continue;
    if not instance_exists(iii) continue;

    if (scr_shouldwrite(iii.object_index)) {    //ignore walls
    obj_name=object_get_name(iii.object_index)+"_"+string(iii.object_index); //(iii.object_index)//
    global.current=iii///ds_list_create()
    which=global.write_called mod 2;
    if which==0 write_arraydata0(iii) else write_arraydata1(iii)

    ds_map_add(frame_data, iii, iii)

    if ds_map_exists(global.previous_frame_data, iii)  {
    //global.previous=ds_map_find_value(global.previous_frame_data, iii);
    compare_result=scr_compare_data(which)
    global.elapsed_time=current_time-global.start_time
    if (compare_result != "")    {
    room_data+=" "+string(obj_name)+"_"+string(iii)+"={"+compare_result+"}, ";  }
    //ds_list_destroy(global.previous);
    } else {
     room_data+=" newInstance("+string(iii)+"),"
    }

    }
  }
  //room_data+=ds_map_write(frame_data)
  room_data+="]
  "
  ds_map_destroy(global.previous_frame_data)
  global.previous_frame_data=frame_data

  return room_data;
#define scr_compare_data
//Compare each instance
if global.framenumber<2 return ""

which=argument0

changed_data=""
var i;
i=0;
var cur,prev;
inst=global.current-100000
 while(i<25) {
 if which == 0 {
      cur=global.array_data0[inst,i];
      prev=global.array_data1[inst,i];
 }
 else {
     cur=global.array_data1[inst,i];
     prev=global.array_data0[inst,i];
     }
 if (cur != prev)   {
 changed_data+=global.localname[i]+":"+string(prev)+"->"+string(cur)+" ";
 }
 i+=1;
 }
 return changed_data;

#define scr_record_input
key = argument0;
frame=argument1;
ds_queue_enqueue(global.input, string(frame) + ":"+string(key)+"
");

#define scr_shouldwrite
//returns whether or not to write this object
inst=argument0
if inst==3 or inst==4 return false

return true

#define scr_write_to_file
fileid=file_text_open_append("/Recorder_data_gm"+string(gamemaker_version)+".txt");

if global.filewrites<1 {file_text_write_string(fileid,scr_write_key());}
global.filewrites+=1;

var i,size;
i=0;
size = ds_queue_size(global.events);
while (i<size) {
event=ds_queue_dequeue(global.events);
file_text_write_string(fileid,event);
i=i+1;
}

//write globals
file_text_write_string(fileid,"globals:{"+scr_write_globals()+"}

")

file_text_close(fileid);
//ds_queue_destroy(events)
#define write_arraydata0
inst=argument0-100000
global.array_data0[inst,0]=iii;
global.array_data0[inst,1]=iii.object_index;
global.array_data0[inst,2]=iii.x;
global.array_data0[inst,3]=iii.y;
global.array_data0[inst,4]=iii.direction;
global.array_data0[inst,5]=iii.speed;
global.array_data0[inst,6]=iii.hspeed;
global.array_data0[inst,7]=iii.vspeed;
global.array_data0[inst,8]=iii.friction;
global.array_data0[inst,9]=iii.gravity;
global.array_data0[inst,10]=iii.gravity_direction;
global.array_data0[inst,11]=iii.sprite_index;
global.array_data0[inst,12]=iii.image_index;
global.array_data0[inst,13]=iii.image_single;
global.array_data0[inst,14]=iii.image_speed;
global.array_data0[inst,15]=0;//iii.image_scale;
global.array_data0[inst,16]=iii.mask_index;
global.array_data0[inst,17]=iii.solid;
global.array_data0[inst,18]=iii.visible;
global.array_data0[inst,19]=iii.persistent;
global.array_data0[inst,20]=iii.depth;
global.array_data0[inst,21]=iii.path_index;
global.array_data0[inst,22]=iii.path_position;
global.array_data0[inst,23]=iii.path_orientation;
global.array_data0[inst,24]=iii.path_scale;

#define scr_get_local_name
localname=argument0
if localname == 0 return "instanceid"
else if localname == 1 return "object_index"
else if localname == 2 return "x"
else if localname == 3 return "y"
else if localname == 4 return "direction"
else if localname == 5 return "speed"
else if localname == 6 return "hspeed"
else if localname == 7 return "vspeed"
else if localname == 8 return "friction"
else if localname == 9 return "gravity"
else if localname == 10 return "gravity_direction"
else if localname == 11 return "sprite_index"
else if localname == 12 return "image_index"
else if localname == 13 return "image_single"
else if localname == 14 return "image_speed"
else if localname == 15 return "image_scale"
else if localname == 16 return "mask_index"
else if localname == 17 return "solid"
else if localname == 18 return "visible"
else if localname == 19 return "persistent"
else if localname == 20 return "depth"
else if localname == 21 return "path_index"
else if localname == 22 return "path_position"
else if localname == 23 return "path_orientation"
else if localname == 24 return "path_scale"
/*data[0]= iii;
    data[1]= iii.object_index;
    data[2]=iii.x;
    data[3]=iii.y;
    data[4]=iii.direction;
    data[5]=iii.speed;
    data[6]=iii.hspeed;
    data[7]=iii.vspeed;
    data[8]=iii.friction;
    data[9]=iii.gravity;
    data[10]=iii.gravity_direction;
    data[11]=iii.sprite_index;
    data[12]=iii.image_index;
    data[13]=iii.image_single;
    data[14]=iii.image_speed;
   // data[15]=iii.image_scale;
    data[16]=iii.mask_index;
    data[17]=iii.solid;
    data[18]=iii.visible;
    data[19]=iii.persistent;
    data[20]=iii.depth;
    data[21]=iii.path_index;
    data[22]=iii.path_position;
    data[23]=iii.path_orientation;
    data[24]=iii.path_scale;
   */

#define write_arraydata1
inst=argument0-100000
global.array_data1[inst,0]=iii;
global.array_data1[inst,1]=iii.object_index;
global.array_data1[inst,2]=iii.x;
global.array_data1[inst,3]=iii.y;
global.array_data1[inst,4]=iii.direction;
global.array_data1[inst,5]=iii.speed;
global.array_data1[inst,6]=iii.hspeed;
global.array_data1[inst,7]=iii.vspeed;
global.array_data1[inst,8]=iii.friction;
global.array_data1[inst,9]=iii.gravity;
global.array_data1[inst,10]=iii.gravity_direction;
global.array_data1[inst,11]=iii.sprite_index;
global.array_data1[inst,12]=iii.image_index;
global.array_data1[inst,13]=iii.image_single;
global.array_data1[inst,14]=iii.image_speed;
global.array_data1[inst,15]=0;//iii.image_scale;
global.array_data1[inst,16]=iii.mask_index;
global.array_data1[inst,17]=iii.solid;
global.array_data1[inst,18]=iii.visible;
global.array_data1[inst,19]=iii.persistent;
global.array_data1[inst,20]=iii.depth;
global.array_data1[inst,21]=iii.path_index;
global.array_data1[inst,22]=iii.path_position;
global.array_data1[inst,23]=iii.path_orientation;
global.array_data1[inst,24]=iii.path_scale;

#define scr_init_localnames
global.localname[0]="instanceid"
global.localname[1]="object_index"
global.localname[2]="x"
global.localname[3]="y"
global.localname[4]="direction"
global.localname[5]="speed"
global.localname[6]="hspeed"
global.localname[7]="vspeed"
global.localname[8]="friction"
global.localname[9]="gravity"
global.localname[10]="gravity_direction"
global.localname[11]="sprite_index"
global.localname[12]="image_index"
global.localname[13]="image_single"
global.localname[14]="image_speed"
global.localname[15]="image_scale"
global.localname[16]="mask_index"
global.localname[17]="solid"
global.localname[18]="visible"
global.localname[19]="persistent"
global.localname[20]="depth"
global.localname[21]="path_index"
global.localname[22]="path_position"
global.localname[23]="path_orientation"
global.localname[24]="path_scale"


#define scr_write_globals
globalsstring=""
which=global.framenumber mod 2;

if which == 0 {
for (i=1; i<87; i+=1) {
 global.global1[i]=scr_get_globalvalue(i)
  if (global.framenumber>1) if (global.global1[i] != global.global2[i]) {
      globalsstring+=global.globalname[i]+"="+string(global.global1[i])+", "
   }
}
}
else {
for (i=1; i<87; i+=1) {
 global.global2[i]=scr_get_globalvalue(i)
   if (global.framenumber>1) if (global.global1[i] != global.global2[i]) {
     globalsstring+=global.globalname[i]+"="+string(global.global2[i])+", "
   }
}
}
return globalsstring;

#define scr_init_globalnames
//globalvar global.globalname;
global.globalname[1]="background_alpha";
global.globalname[2]="background_blend";
global.globalname[3]="background_color";
global.globalname[4]="background_foreground";
global.globalname[5]="background_height";
global.globalname[6]="background_hspeed";
global.globalname[7]="background_htiled";
global.globalname[8]="background_index";
global.globalname[9]="background_showcolor";
global.globalname[10]="background_visible";
global.globalname[11]="background_vspeed";
global.globalname[12]="background_vtiled";
global.globalname[13]="background_width";
global.globalname[14]="background_x";
global.globalname[15]="background_xscale";
global.globalname[16]="background_y";
global.globalname[17]="background_yscale";
global.globalname[18]="caption_health";
global.globalname[19]="caption_lives";
global.globalname[20]="caption_score";
global.globalname[21]="current_day";
global.globalname[22]="current_hour";
global.globalname[23]="current_minute";
global.globalname[24]="current_month";
global.globalname[25]="current_second";
global.globalname[26]="current_time";
global.globalname[27]="current_weekday";
global.globalname[28]="current_year";
global.globalname[29]="cursor_sprite";
global.globalname[30]="error_last";
global.globalname[31]="error_occurred";
global.globalname[32]="event_action";
global.globalname[33]="event_number";
global.globalname[34]="event_object";
global.globalname[35]="event_type";
global.globalname[36]="fps";
global.globalname[37]="game_id";
global.globalname[38]="gamemaker_version";
global.globalname[39]="health";
global.globalname[40]="instance_count";
global.globalname[41]="instance_id";
global.globalname[42]="keyboard_key";
global.globalname[43]="keyboard_lastchar";
global.globalname[44]="keyboard_lastkey";
global.globalname[45]="keyboard_string";
global.globalname[46]="lives";
global.globalname[47]="mouse_button";
global.globalname[48]="mouse_lastbutton";
global.globalname[49]="mouse_x";
global.globalname[50]="mouse_y";
global.globalname[51]="os_type";
global.globalname[52]="program_directory";
global.globalname[53]="room";
global.globalname[54]="room_caption";
global.globalname[55]="room_first";
global.globalname[56]="room_height";
global.globalname[57]="room_last";
global.globalname[58]="room_persistent";
global.globalname[59]="room_speed";
global.globalname[60]="room_width";
global.globalname[61]="score";
global.globalname[62]="secure_mode";
global.globalname[63]="show_health";
global.globalname[64]="show_lives";
global.globalname[65]="show_score";
global.globalname[66]="temp_directory";
global.globalname[67]="transition_kind";
global.globalname[68]="transition_steps";
global.globalname[69]="view_angle";
global.globalname[70]="view_current";
global.globalname[71]="view_enabled";
global.globalname[72]="view_hborder";
global.globalname[73]="view_hport";
global.globalname[74]="view_hspeed";
global.globalname[75]="view_hview";
global.globalname[76]="view_object";
global.globalname[77]="view_vborder";
global.globalname[78]="view_visible";
global.globalname[79]="view_vspeed";
global.globalname[80]="view_wport";
global.globalname[81]="view_wview";
global.globalname[82]="view_xport";
global.globalname[83]="view_xview";
global.globalname[84]="view_yport";
global.globalname[85]="view_yview";
global.globalname[86]="working_directory";

#define scr_get_globalvalue
if argument0==1 return  background_alpha;
else if argument0==2 return  background_blend;
else if argument0==3 return  background_color;
else if argument0==4 return  background_foreground;
else if argument0==5 return  background_height;
else if argument0==6 return  background_hspeed;
else if argument0==7 return  background_htiled;
else if argument0==8 return  background_index;
else if argument0==9 return  background_showcolor;
else if argument0==10 return  background_visible;
else if argument0==11 return  background_vspeed;
else if argument0==12 return  background_vtiled;
else if argument0==13 return  background_width;
else if argument0==14 return  background_x;
else if argument0==15 return  background_xscale;
else if argument0==16 return  background_y;
else if argument0==17 return  background_yscale;
else if argument0==18 return  caption_health;
else if argument0==19 return  caption_lives;
else if argument0==20 return  caption_score;
else if argument0==21 return  current_day;
else if argument0==22 return  current_hour;
else if argument0==23 return  current_minute;
else if argument0==24 return  current_month;
else if argument0==25 return  current_second;
else if argument0==26 return  current_time;
else if argument0==27 return  current_weekday;
else if argument0==28 return  current_year;
else if argument0==29 return  cursor_sprite;
else if argument0==30 return  error_last;
else if argument0==31 return  error_occurred;
else if argument0==32 return  event_action;
else if argument0==33 return  event_number;
else if argument0==34 return  event_object;
else if argument0==35 return  event_type;
else if argument0==36 return  fps;
else if argument0==37 return  game_id;
else if argument0==38 return  gamemaker_version;
else if argument0==39 return  health;
else if argument0==40 return  instance_count;
else if argument0==41 return 0;//return  instance_id;
else if argument0==42 return  keyboard_key;
else if argument0==43 return  keyboard_lastchar;
else if argument0==44 return  keyboard_lastkey;
else if argument0==45 return  keyboard_string;
else if argument0==46 return  lives;
else if argument0==47 return  mouse_button;
else if argument0==48 return  mouse_lastbutton;
else if argument0==49 return  mouse_x;
else if argument0==50 return  mouse_y;
else if argument0==51 return  os_type;
else if argument0==52 return  program_directory;
else if argument0==53 return  room;
else if argument0==54 return  room_caption;
else if argument0==55 return  room_first;
else if argument0==56 return  room_height;
else if argument0==57 return  room_last;
else if argument0==58 return  room_persistent;
else if argument0==59 return  room_speed;
else if argument0==60 return  room_width;
else if argument0==61 return  score;
else if argument0==62 return  secure_mode;
else if argument0==63 return  show_health;
else if argument0==64 return  show_lives;
else if argument0==65 return  show_score;
else if argument0==66 return  temp_directory;
else if argument0==67 return  transition_kind;
else if argument0==68 return  transition_steps;
else if argument0==69 return  view_angle;
else if argument0==70 return  view_current;
else if argument0==71 return  view_enabled;
else if argument0==72 return  view_hborder;
else if argument0==73 return  view_hport;
else if argument0==74 return  view_hspeed;
else if argument0==75 return  view_hview;
else if argument0==76 return  view_object;
else if argument0==77 return  view_vborder;
else if argument0==78 return  view_visible;
else if argument0==79 return  view_vspeed;
else if argument0==80 return  view_wport;
else if argument0==81 return  view_wview;
else if argument0==82 return  view_xport;
else if argument0==83 return  view_xview;
else if argument0==84 return  view_yport;
else if argument0==85 return  view_yview;
else if argument0==86 return  working_directory;

#define scr_write_key
//writes a key at the top of the file
var game_key,ignoring,writing;
game_key="Recorder key:"
ignoring=""
writing=""
for (i=0; i<instance_count; i+=1)
  {
    iii = instance_id[i];
    if (scr_shouldwrite(iii.object_index)) {
    writing+=object_get_name(iii.object_index)+"("+string(iii.object_index)+"), ";
    } else ignoring+=object_get_name(iii.object_index)+"("+string(iii.object_index)+"), ";
  }

  game_key+="ignoring: "+ignoring+"
  "
  game_key+="writing: "+writing+"
  "

  //write all globals
  game_key+="
  Initial global values:"
  for (i=1; i<87; i+=1) {
      game_key+=global.globalname[i]+"="+string(scr_get_globalvalue(i))+", "
  }
return game_key+"
"

#define scr_init_recorder
//if (global.init_recorder==true) return 0;
file_delete("/Recorder_data_gm"+string(gamemaker_version)+".txt")

show_message("Recorder started");
//globalvar events;
global.elapsed_time=0;

global.array_data0[0,0]=0
global.array_data1[0,0]=0

global.write_called=0;
global.filewrites=0;

global.global1[88]=-1
global.global2[88]=-1

global.events=ds_queue_create();
global.input=ds_queue_create();
global.previous_frame_data=ds_map_create(); //start with a blank frame
scr_init_localnames();
scr_init_globalnames();

global.framenumber=0;

//cheat a bit
lives=100;

global.init_recorder=true

