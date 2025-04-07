"""
example_html_responses.py
Author: https://github.com/lendrixxx
Description: This file defines example HTML responses for Barrys.
"""
EXAMPLE_RAFFLES_AND_ORCHARD_HTML_RESPONSE = """
<ul class="nav nav-pills" id="reserveFilter">
    <li class="dropdown" id="reserveFilter1">
        <a class="dropdown-toggle" data-toggle="dropdown" href="#reserveFilter1">By Instructor
            <b class="caret"></b></a>
        <ul class="dropdown-menu">
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=2357132732833728308&amp;site2=12">Ambika
                    Chanrai</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=1962218357339981238&amp;site2=12">Gino
                    Morales</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=882162166147318961&amp;site2=12">Ian
                    Chan</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=882077773613500377&amp;site2=12">Instructor
                    TBD</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=1868869165436110674&amp;site2=12">Jess
                    Arrowsmith</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=1485105934370866912&amp;site2=12">Jian
                    Hong Teng</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=2437831291320665860&amp;site2=12">Jona
                    Mae De Gollo</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=1996750998659401697&amp;site2=12">Joyee
                    Tan</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=2434862017094354475&amp;site2=12">Kenny
                    Ng</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=996639398235735055&amp;site2=12">Kim
                    Eusope</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=882162518837953821&amp;site2=12">Lorna
                    da Costa</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=1962219855704753655&amp;site2=12">Mandalyn
                    Tan</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=2434144339778078209&amp;site2=12">Nerissa
                    Ngein</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=1575295622502680332&amp;site2=12">Ria
                    Chen</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=1575296829229107001&amp;site2=12">Shannon
                    Stephen</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;instructorid=1488914369566737506&amp;site2=12">Stephanie
                    Shabanov</a></li>
        </ul>
    </li>
    <li class="dropdown" id="reserveFilter2">
        <a class="dropdown-toggle" data-toggle="dropdown" href="#reserveFilter2">By Class
            <b class="caret"></b></a>
        <ul class="dropdown-menu">
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;classtypeid=882169365309425202&amp;site2=12">Abs
                    & Ass (50 min)</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;classtypeid=698312905870804011&amp;site2=12">Arms
                    & Abs (50 min)</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;classtypeid=875886255454291221&amp;site2=12">Chest,
                    Back & Abs (50 min)</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;classtypeid=829450263361226558&amp;site2=12">Full
                    Body (Lower Focus) (50 min)</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;classtypeid=830918605154550914&amp;site2=12">Full
                    Body (Upper Focus) (50 min)</a></li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;classtypeid=830197022001727052&amp;site2=12">Total
                    Body (50 min)</a></li>
        </ul>
    </li>
    <li class="dropdown" id="reserveFilter3">
        <a class="dropdown-toggle" data-toggle="dropdown" href="#reserveFilter3">By Room
            <b class="caret"></b></a>
        <ul class="dropdown-menu">
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;roomid=1232806668564170202&amp;site2=12">Orchard</a>
            </li>
            <li><a
                    href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;roomid=832424681775564623&amp;site2=12">Raffles
                    Place</a></li>
        </ul>
    </li>
    <li class="dropdown hidden" id="reserveFilterSites">
        <a class="dropdown-toggle" data-toggle="dropdown" href="#reserveFilterSites">By Location
            <b class="caret"></b></a>
        <ul class="dropdown-menu">
            <li><a href="index.cfm?action=Reserve.chooseClass&amp;site=1">Raffles Place</a></li>
            <li><a href="index.cfm?action=Reserve.chooseClass&amp;site=12">Orchard</a></li>
        </ul>
    </li>
</ul>
<ul id="reserveweeknav" class="pager">
    <li class="previous disabled"><a href="#"><span>Prev Week</span></a></li>
    <li class="next"><a
            href="index.cfm?action=Reserve.chooseClass&amp;site=1&amp;site2=12&amp;wk=1"><span>Next Week</span></a>
    </li>
</ul>
<div id="reservedays">
    <ul class="nav nav-tabs hidden-phone">
        <li class="active"><a href="#day20250407"
                data-toggle="tab"><span class="tab-dow">Mon</span><span class="tab-date">07.04</span></a>
        </li>
        <li><a href="#day20250408"
                data-toggle="tab"><span class="tab-dow">Tue</span><span class="tab-date">08.04</span></a>
        </li>
        <li><a href="#day20250409"
                data-toggle="tab"><span class="tab-dow">Wed</span><span class="tab-date">09.04</span></a>
        </li>
        <li><a href="#day20250410"
                data-toggle="tab"><span class="tab-dow">Thu</span><span class="tab-date">10.04</span></a>
        </li>
        <li><a href="#day20250411"
                data-toggle="tab"><span class="tab-dow">Fri</span><span class="tab-date">11.04</span></a>
        </li>
        <li><a href="#day20250412"
                data-toggle="tab"><span class="tab-dow">Sat</span><span class="tab-date">12.04</span></a>
        </li>
        <li><a href="#day20250413"
                data-toggle="tab"><span class="tab-dow">Sun</span><span class="tab-date">13.04</span></a>
        </li>
    </ul>
    <div class="btn-group hidden-desktop hidden-tablet">
        <a class="btn btn-block dropdown-toggle" data-toggle="dropdown"
            href="#"><span class="tab-dow">Mon</span><span class="tab-date">07.04</span>
            <span class="caret"></span></a>
        <ul class="dropdown-menu">
            <li class="active"><a href="#day20250407"
                    data-toggle="tab"><span class="tab-dow">Mon</span><span class="tab-date">07.04</span></a>
            </li>
            <li><a href="#day20250408"
                    data-toggle="tab"><span class="tab-dow">Tue</span><span class="tab-date">08.04</span></a>
            </li>
            <li><a href="#day20250409"
                    data-toggle="tab"><span class="tab-dow">Wed</span><span class="tab-date">09.04</span></a>
            </li>
            <li><a href="#day20250410"
                    data-toggle="tab"><span class="tab-dow">Thu</span><span class="tab-date">10.04</span></a>
            </li>
            <li><a href="#day20250411"
                    data-toggle="tab"><span class="tab-dow">Fri</span><span class="tab-date">11.04</span></a>
            </li>
            <li><a href="#day20250412"
                    data-toggle="tab"><span class="tab-dow">Sat</span><span class="tab-date">12.04</span></a>
            </li>
            <li><a href="#day20250413"
                    data-toggle="tab"><span class="tab-dow">Sun</span><span class="tab-date">13.04</span></a>
            </li>
        </ul>
    </div>
</div>
<div class="tab-content reservelist">
    <div class="tab-pane active" id="day20250407">
        <h3>Monday, 7 April 2025</h3>
        <div class="scheduleBlock" data-room="832424681775564623"
            data-classtype="698312905870804011" data-instructor="2357132732833728308"
            data-classid="2437629699724150211">
            <div class="row-fluid">
                <span class="span1 scheduleTime"><span>6:30 AM</span></span>
                <span class="span2 scheduleSite">Raffles Place</span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span></span>
                <span class="span3 scheduleInstruc"><span>Ambika Chanrai</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </div>
        </div>
        <div class="scheduleBlock" data-room="1232806668564170202"
            data-classtype="698312905870804011" data-instructor="1962219855704753655"
            data-classid="2418737466119816865">
            <div class="row-fluid">
                <span class="span1 scheduleTime"><span>7:00 AM</span></span>
                <span class="span2 scheduleSite">Orchard</span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span></span>
                <span class="span3 scheduleInstruc"><span>Mandalyn Tan</span>
                <i class="badge substitute" title="Substitute for Shannon Stephen">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </div>
        </div>
        <div class="scheduleBlock" data-room="832424681775564623"
            data-classtype="698312905870804011" data-instructor="1488914369566737506"
            data-classid="2437629699875145156">
            <div class="row-fluid">
                <span class="span1 scheduleTime"><span>7:30 AM</span></span>
                <span class="span2 scheduleSite">Raffles Place</span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span></span>
                <span class="span3 scheduleInstruc"><span>Stephanie Shabanov</span>
                <i class="badge substitute" title="Substitute for Kim Eusope">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </div>
        </div>
        <div class="scheduleBlock" data-room="1232806668564170202"
            data-classtype="698312905870804011" data-instructor="996639398235735055"
            data-classid="2418737466228868770">
            <div class="row-fluid">
                <span class="span1 scheduleTime"><span>8:05 AM</span></span>
                <span class="span2 scheduleSite">Orchard</span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span></span>
                <span class="span3 scheduleInstruc"><span>Kim Eusope</span>
                <i class="badge substitute" title="Substitute for Stephanie Shabanov">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </div>
        </div>
        <div class="scheduleBlock" data-room="832424681775564623"
            data-classtype="698312905870804011" data-instructor="1962218357339981238"
            data-classid="2437629700017751493">
            <div class="row-fluid">
                <span class="span1 scheduleTime"><span>8:30 AM</span></span>
                <span class="span2 scheduleSite">Raffles Place</span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span></span>
                <span class="span3 scheduleInstruc"><span>Gino Morales</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </div>
        </div>
        <div class="scheduleBlock" data-room="1232806668564170202"
            data-classtype="698312905870804011" data-instructor="882162166147318961"
            data-classid="2418737466337920675">
            <div class="row-fluid">
                <span class="span1 scheduleTime"><span>9:15 AM</span></span>
                <span class="span2 scheduleSite">Orchard</span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span></span>
                <span class="span3 scheduleInstruc"><span>Ian Chan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </div>
        </div>
        <div class="scheduleBlock" data-room="1232806668564170202"
            data-classtype="698312905870804011" data-instructor="996639398235735055"
            data-classid="2418737466480527012">
            <div class="row-fluid">
                <span class="span1 scheduleTime"><span>10:15 AM</span></span>
                <span class="span2 scheduleSite">Orchard</span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span></span>
                <span class="span3 scheduleInstruc"><span>Kim Eusope</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </div>
        </div>
        <div class="scheduleBlock" data-room="832424681775564623"
            data-classtype="698312905870804011" data-instructor="1488914369566737506"
            data-classid="2437629700235855302">
            <div class="row-fluid">
                <span class="span1 scheduleTime"><span>11:15 AM</span></span>
                <span class="span2 scheduleSite">Raffles Place</span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span></span>
                <span class="span3 scheduleInstruc"><span>Stephanie Shabanov</span>
                <i class="badge substitute" title="Substitute for Shannon Stephen">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </div>
        </div>
        <div class="scheduleBlock" data-room="832424681775564623"
            data-classtype="698312905870804011" data-instructor="1962218357339981238"
            data-classid="2437629700479124935">
            <div class="row-fluid">
                <span class="span1 scheduleTime"><span>12:15 PM</span></span>
                <span class="span2 scheduleSite">Raffles Place</span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span></span>
                <span class="span3 scheduleInstruc"><span>Gino Morales</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </div>
        </div>
        <div class="scheduleBlock" data-room="1232806668564170202"
            data-classtype="698312905870804011" data-instructor="2357132732833728308"
            data-classid="2418737466639910565">
            <div class="row-fluid">
                <span class="span1 scheduleTime"><span>12:15 PM</span></span>
                <span class="span2 scheduleSite">Orchard</span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span></span>
                <span class="span3 scheduleInstruc"><span>Ambika Chanrai</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </div>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="698312905870804011" data-instructor="1488914369566737506"
            data-classid="2437629700672062920">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629700672062920"
                data-haslayout="true" data-name="Arms & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>5:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span>
                <i class="icon-info-sign pop" data-classtype="698312905870804011" data-classid="2437629700672062920" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Stephanie Shabanov</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="698312905870804011" data-instructor="1575295622502680332"
            data-classid="2418737466782516902">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2418737466782516902"
                data-haslayout="true" data-name="Arms & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span>
                <i class="icon-info-sign pop" data-classtype="698312905870804011" data-classid="2418737466782516902" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ria Chen</span>
                <i class="badge substitute" title="Substitute for Ria Chen">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock  classfull" data-room="832424681775564623"
            data-classtype="698312905870804011" data-instructor="882162166147318961"
            data-classid="2437629700865000905">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629700865000905"
                data-haslayout="true" data-name="Arms & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="badge waitlist" title="Class Full - waitlist available">W</i>
                <span class="span1 scheduleTime"><span>6:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span>
                <i class="icon-info-sign pop" data-classtype="698312905870804011" data-classid="2437629700865000905" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ian Chan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="698312905870804011" data-instructor="1962218357339981238"
            data-classid="2418737466950289063">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2418737466950289063"
                data-haslayout="true" data-name="Arms & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span>
                <i class="icon-info-sign pop" data-classtype="698312905870804011" data-classid="2418737466950289063" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Gino Morales</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock  classfull" data-room="832424681775564623"
            data-classtype="698312905870804011" data-instructor="1575295622502680332"
            data-classid="2437629701057938890">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629701057938890"
                data-haslayout="true" data-name="Arms & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="badge waitlist" title="Class Full - waitlist available">W</i>
                <span class="span1 scheduleTime"><span>7:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span>
                <i class="icon-info-sign pop" data-classtype="698312905870804011" data-classid="2437629701057938890" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ria Chen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="698312905870804011" data-instructor="2434144339778078209"
            data-classid="2418737467076118184">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2418737467076118184"
                data-haslayout="true" data-name="Arms & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Arms & Abs</span>
                <i class="icon-info-sign pop" data-classtype="698312905870804011" data-classid="2418737467076118184" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Nerissa Ngein</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
    </div>
    <div class="tab-pane" id="day20250408">
        <h3>Tuesday, 8 April 2025</h3>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="829450263361226558" data-instructor="1575295622502680332"
            data-classid="2437630546679957391">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630546679957391"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437630546679957391" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ria Chen</span>
                <i class="badge substitute" title="Substitute for Shannon Stephen">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="829450263361226558" data-instructor="1996750998659401697"
            data-classid="2437629024642532477">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629024642532477"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:00 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437629024642532477" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Joyee Tan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="829450263361226558" data-instructor="1488914369566737506"
            data-classid="2437630546856118160">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630546856118160"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437630546856118160" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Stephanie Shabanov</span>
                <i class="badge substitute" title="Substitute for Jess Arrowsmith">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="829450263361226558" data-instructor="1962219855704753655"
            data-classid="2437629024827081854">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629024827081854"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:05 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437629024827081854" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Mandalyn Tan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="829450263361226558" data-instructor="2434144339778078209"
            data-classid="2437630547023890321">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630547023890321"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437630547023890321" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Nerissa Ngein</span>
                <i class="badge substitute" title="Substitute for Cassandra Mai">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="829450263361226558" data-instructor="996639398235735055"
            data-classid="2437629025036797055">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629025036797055"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>9:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437629025036797055" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Kim Eusope</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="829450263361226558" data-instructor="1575295622502680332"
            data-classid="2437629025263289472">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629025263289472"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>10:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437629025263289472" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ria Chen</span>
                <i class="badge substitute" title="Substitute for Shannon Stephen">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="829450263361226558" data-instructor="996639398235735055"
            data-classid="2437630547216828306">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630547216828306"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>11:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437630547216828306" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Kim Eusope</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="829450263361226558" data-instructor="1575295622502680332"
            data-classid="2437629025481393282">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629025481393282"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:15 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437629025481393282" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ria Chen</span>
                <i class="badge substitute" title="Substitute for Cassandra Mai">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="829450263361226558" data-instructor="1996750998659401697"
            data-classid="2437630547653035924">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630547653035924"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>5:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437630547653035924" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Joyee Tan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="829450263361226558" data-instructor="1488914369566737506"
            data-classid="2437629025707885699">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629025707885699"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437629025707885699" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Stephanie Shabanov</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="829450263361226558" data-instructor="1962219855704753655"
            data-classid="2437630547854362517">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630547854362517"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437630547854362517" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Mandalyn Tan</span>
                <i class="badge substitute" title="Substitute for Shannon Stephen">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="829450263361226558" data-instructor="996639398235735055"
            data-classid="2437629025925989509">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629025925989509"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437629025925989509" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Kim Eusope</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="829450263361226558" data-instructor="1962219855704753655"
            data-classid="2437630548047300502">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630548047300502"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437630548047300502" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Mandalyn Tan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="829450263361226558" data-instructor="2437831291320665860"
            data-classid="2437629026110538886">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437629026110538886"
                data-haslayout="true" data-name="Full Body (Lower Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Lower Focus)</span>
                <i class="icon-info-sign pop" data-classtype="829450263361226558" data-classid="2437629026110538886" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Jona Mae De Gollo</span>
                <i class="badge substitute" title="Substitute for Jona Mae De Gollo">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
    </div>
    <div class="tab-pane" id="day20250409">
        <h3>Wednesday, 9 April 2025</h3>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="875886255454291221" data-instructor="882162518837953821"
            data-classid="2437630668591597535">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630668591597535"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437630668591597535" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Lorna da Costa</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="875886255454291221" data-instructor="1488914369566737506"
            data-classid="2437631234378040780">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631234378040780"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:00 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437631234378040780" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Stephanie Shabanov</span>
                <i class="badge substitute" title="Substitute for Jess Arrowsmith">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="875886255454291221" data-instructor="882162518837953821"
            data-classid="2437630668784535520">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630668784535520"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437630668784535520" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Lorna da Costa</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="875886255454291221" data-instructor="1575295622502680332"
            data-classid="2437631234545812942">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631234545812942"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:05 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437631234545812942" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ria Chen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="875886255454291221" data-instructor="2437831291320665860"
            data-classid="2437630668960696289">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630668960696289"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437630668960696289" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Jona Mae De Gollo</span>
                <i class="badge substitute" title="Substitute for Kenny Ng">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="875886255454291221" data-instructor="1575296829229107001"
            data-classid="2437631234696807889">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631234696807889"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>9:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437631234696807889" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Shannon Stephen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="875886255454291221" data-instructor="2434144339778078209"
            data-classid="2437631234839414227">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631234839414227"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>10:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437631234839414227" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Nerissa Ngein</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="875886255454291221" data-instructor="1575295622502680332"
            data-classid="2437630669178800098">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630669178800098"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>11:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437630669178800098" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ria Chen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="875886255454291221" data-instructor="1575296829229107001"
            data-classid="2437630669430458339">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630669430458339"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:15 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437630669430458339" data-customtype="Chest, Back & Abs"></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Shannon Stephen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="875886255454291221" data-instructor="882162518837953821"
            data-classid="2437631235040740821">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631235040740821"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:15 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437631235040740821" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Lorna da Costa</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="875886255454291221" data-instructor="1488914369566737506"
            data-classid="2437630669656950756">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630669656950756"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>5:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437630669656950756" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Stephanie Shabanov</span>
                <i class="badge substitute" title="Substitute for Jess Arrowsmith">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="875886255454291221" data-instructor="882162518837953821"
            data-classid="2437631235216901591">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631235216901591"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437631235216901591" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Lorna da Costa</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="875886255454291221" data-instructor="1962219855704753655"
            data-classid="2437630669875054565">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630669875054565"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437630669875054565" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Mandalyn Tan</span>
                <i class="badge substitute" title="Substitute for Cassandra Mai">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="875886255454291221" data-instructor="1575296829229107001"
            data-classid="2437631235393062361">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631235393062361"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437631235393062361" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Shannon Stephen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="875886255454291221" data-instructor="2434144339778078209"
            data-classid="2437630670101546982">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630670101546982"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437630670101546982" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Nerissa Ngein</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="875886255454291221" data-instructor="1575295622502680332"
            data-classid="2437631235569223131">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631235569223131"
                data-haslayout="true" data-name="Chest, Back & Abs" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Chest, Back & Abs</span>
                <i class="icon-info-sign pop" data-classtype="875886255454291221" data-classid="2437631235569223131" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ria Chen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
    </div>
    <div class="tab-pane" id="day20250410">
        <h3>Thursday, 10 April 2025</h3>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="882169365309425202" data-instructor="1962218357339981238"
            data-classid="2437630741387936789">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630741387936789"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437630741387936789" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Gino Morales</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="882169365309425202" data-instructor="2357132732833728308"
            data-classid="2437632688107029984">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437632688107029984"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:00 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437632688107029984" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ambika Chanrai</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="882169365309425202" data-instructor="882162166147318961"
            data-classid="2437630741538931734">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630741538931734"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437630741538931734" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ian Chan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="882169365309425202" data-instructor="1962218357339981238"
            data-classid="2437632688258024929">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437632688258024929"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:05 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437632688258024929" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Gino Morales</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="882169365309425202" data-instructor="2357132732833728308"
            data-classid="2437630741698315287">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630741698315287"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437630741698315287" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ambika Chanrai</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="882169365309425202" data-instructor="1962219855704753655"
            data-classid="2437632688400631266">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437632688400631266"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>9:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437632688400631266" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Mandalyn Tan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="882169365309425202" data-instructor="1575295622502680332"
            data-classid="2437632688543237603">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437632688543237603"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>10:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437632688543237603" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ria Chen</span>
                <i class="badge substitute" title="Substitute for Instructor TBD">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="882169365309425202" data-instructor="1996750998659401697"
            data-classid="2437630741874476056">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630741874476056"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>11:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437630741874476056" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Joyee Tan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="882169365309425202" data-instructor="882162166147318961"
            data-classid="2437630742084191257">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630742084191257"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:15 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437630742084191257" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ian Chan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="882169365309425202" data-instructor="1575296829229107001"
            data-classid="2437632688719398372">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437632688719398372"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:15 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437632688719398372" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Shannon Stephen</span>
                <i class="badge substitute" title="Substitute for Stephanie Shabanov">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="882169365309425202" data-instructor="996639398235735055"
            data-classid="2437630742260352026">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630742260352026"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>5:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437630742260352026" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Kim Eusope</span>
                <i class="badge substitute" title="Substitute for Jess Arrowsmith">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="882169365309425202" data-instructor="1996750998659401697"
            data-classid="2437632688853616101">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437632688853616101"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437632688853616101" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Joyee Tan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="882169365309425202" data-instructor="1575296829229107001"
            data-classid="2437630742428124187">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630742428124187"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437630742428124187" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Shannon Stephen</span>
                <i class="badge substitute" title="Substitute for Stephanie Shabanov">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="882169365309425202" data-instructor="1962219855704753655"
            data-classid="2437632689029776870">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437632689029776870"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437632689029776870" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Mandalyn Tan</span>
                <i class="badge substitute" title="Substitute for Jess Arrowsmith">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="882169365309425202" data-instructor="2434144339778078209"
            data-classid="2437630742604284956">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630742604284956"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437630742604284956" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Nerissa Ngein</span>
                <i class="badge substitute" title="Substitute for Kenny Ng">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="882169365309425202" data-instructor="882162166147318961"
            data-classid="2437632689180771815">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437632689180771815"
                data-haslayout="true" data-name="Abs & Ass" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:00 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Abs & Ass</span>
                <i class="icon-info-sign pop" data-classtype="882169365309425202" data-classid="2437632689180771815" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ian Chan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
    </div>
    <div class="tab-pane" id="day20250411">
        <h3>Friday, 11 April 2025</h3>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="882162166147318961"
            data-classid="2437630935592600702">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630935592600702"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437630935592600702" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ian Chan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="1962219855704753655"
            data-classid="2437633131252025098">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633131252025098"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:00 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437633131252025098" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Mandalyn Tan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="1575295622502680332"
            data-classid="2437630935710041215">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630935710041215"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437630935710041215" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ria Chen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="882162166147318961"
            data-classid="2437633131428185867">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633131428185867"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:05 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437633131428185867" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ian Chan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="2434144339778078209"
            data-classid="2437630935835870336">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630935835870336"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437630935835870336" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Nerissa Ngein</span>
                <i class="badge substitute" title="Substitute for Mandalyn Tan">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="996639398235735055"
            data-classid="2437633131604346636">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633131604346636"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>9:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437633131604346636" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Kim Eusope</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="882162166147318961"
            data-classid="2437633131814061837">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633131814061837"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>10:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437633131814061837" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ian Chan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="1575296829229107001"
            data-classid="2437630935978476673">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630935978476673"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>11:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437630935978476673" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Shannon Stephen</span>
                <i class="badge substitute" title="Substitute for Jona Mae De Gollo">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="996639398235735055"
            data-classid="2437630936146248834">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630936146248834"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:15 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437630936146248834" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Kim Eusope</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="1996750998659401697"
            data-classid="2437633132023777038">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633132023777038"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:15 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437633132023777038" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Joyee Tan</span>
                <i class="badge substitute" title="Substitute for Ria Chen">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="1962219855704753655"
            data-classid="2437633132250269455">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633132250269455"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>5:15 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437633132250269455" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Mandalyn Tan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="1575296829229107001"
            data-classid="2437630936297243779">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630936297243779"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>5:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437630936297243779" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Shannon Stephen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="1962219855704753655"
            data-classid="2437633132451596048">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633132451596048"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:15 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437633132451596048" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Mandalyn Tan</span>
                <i class="badge substitute" title="Substitute for Kenny Ng">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="2437831291320665860"
            data-classid="2437630936473404548">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437630936473404548"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>6:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437630936473404548" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Jona Mae De Gollo</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="1575296829229107001"
            data-classid="2437633132678088465">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633132678088465"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>7:15 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437633132678088465" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Shannon Stephen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
    </div>
    <div class="tab-pane" id="day20250412">
        <h3>Saturday, 12 April 2025</h3>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830918605154550914" data-instructor="882077773613500377"
            data-classid="2437633868510004422">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633868510004422"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:00 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437633868510004422" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Instructor TBD</span>
                <i class="badge substitute" title="Substitute for Stephanie Shabanov">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830918605154550914" data-instructor="1868869165436110674"
            data-classid="2437631039208686795">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631039208686795"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437631039208686795" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Jess Arrowsmith</span>
                <i class="badge substitute" title="Substitute for Jess Arrowsmith">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830918605154550914" data-instructor="882162166147318961"
            data-classid="2437633868652610759">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633868652610759"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>9:05 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437633868652610759" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ian Chan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830918605154550914" data-instructor="1485105934370866912"
            data-classid="2437631039510676684">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631039510676684"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>9:35 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437631039510676684" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Jian Hong Teng</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830918605154550914" data-instructor="1868869165436110674"
            data-classid="2437633868795217096">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633868795217096"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>10:10 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437633868795217096" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Jess Arrowsmith</span>
                <i class="badge substitute" title="Substitute for Jess Arrowsmith">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830918605154550914" data-instructor="1962218357339981238"
            data-classid="2437631039703614669">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631039703614669"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>10:40 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437631039703614669" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Gino Morales</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830918605154550914" data-instructor="1485105934370866912"
            data-classid="2437633868937823433">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633868937823433"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>11:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437633868937823433" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Jian Hong Teng</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830918605154550914" data-instructor="2434144339778078209"
            data-classid="2437631039888164046">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631039888164046"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>11:45 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437631039888164046" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Nerissa Ngein</span>
                <i class="badge substitute" title="Substitute for Ria Chen">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830918605154550914" data-instructor="1962218357339981238"
            data-classid="2437633869080429770">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633869080429770"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:20 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437633869080429770" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Gino Morales</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830918605154550914" data-instructor="882162166147318961"
            data-classid="2437631040064324815">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631040064324815"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:50 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437631040064324815" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Ian Chan</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830918605154550914" data-instructor="2434144339778078209"
            data-classid="2437633869223036107">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633869223036107"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>1:25 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437633869223036107" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Nerissa Ngein</span>
                <i class="badge substitute" title="Substitute for Ria Chen">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830918605154550914" data-instructor="2434144339778078209"
            data-classid="2437633869365642444">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633869365642444"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>2:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437633869365642444" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Nerissa Ngein</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830918605154550914" data-instructor="2434862017094354475"
            data-classid="2437633869516637389">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437633869516637389"
                data-haslayout="true" data-name="Full Body (Upper Focus)" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>3:35 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Full Body (Upper Focus)</span>
                <i class="icon-info-sign pop" data-classtype="830918605154550914" data-classid="2437633869516637389" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Kenny Ng</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
    </div>
    <div class="tab-pane" id="day20250413">
        <h3>Sunday, 13 April 2025</h3>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="882162518837953821"
            data-classid="2437631214933247302">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631214933247302"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>8:30 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437631214933247302" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Lorna da Costa</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="1575296829229107001"
            data-classid="2437635023059289945">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437635023059289945"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>9:05 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437635023059289945" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Shannon Stephen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="882162518837953821"
            data-classid="2437631215075853639">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631215075853639"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>9:35 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437631215075853639" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Lorna da Costa</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="996639398235735055"
            data-classid="2437635023227062106">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437635023227062106"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>10:10 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437635023227062106" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Kim Eusope</span>
                <i class="badge substitute" title="Substitute for Stephanie Shabanov">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="1575296829229107001"
            data-classid="2437631215226848584">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631215226848584"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>10:40 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437631215226848584" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Shannon Stephen</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="882162518837953821"
            data-classid="2437635023386445659">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437635023386445659"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>11:15 AM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437635023386445659" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Lorna da Costa</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="996639398235735055"
            data-classid="2437631215377843529">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631215377843529"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>11:45 AM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437631215377843529" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Kim Eusope</span>
                <i class="badge substitute" title="Substitute for Stephanie Shabanov">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="2437831291320665860"
            data-classid="2437635023545829212">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437635023545829212"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:20 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437635023545829212" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Jona Mae De Gollo</span>
                <i class="badge substitute" title="Substitute for Instructor TBD">S</i></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="832424681775564623"
            data-classtype="830197022001727052" data-instructor="1485105934370866912"
            data-classid="2437631215512061258">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437631215512061258"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>12:50 PM</span></span>
                <span class="span2 scheduleSite"><span>Raffles Place</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437631215512061258" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Jian Hong Teng</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="2434144339778078209"
            data-classid="2437635023713601373">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437635023713601373"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>1:25 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437635023713601373" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Nerissa Ngein</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="882162518837953821"
            data-classid="2437635023881373534">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437635023881373534"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>2:30 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437635023881373534" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Lorna da Costa</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
        <div class="scheduleBlock " data-room="1232806668564170202"
            data-classtype="830197022001727052" data-instructor="1485105934370866912"
            data-classid="2437635024040757087">
            <a href="index.cfm?action=Reserve.chooseSpot&amp;classid=2437635024040757087"
                data-haslayout="true" data-name="Total Body" data-site="Raffles Place"
                class="row-fluid">
                <i class="icon-chevron-right"></i>
                <span class="span1 scheduleTime"><span>3:35 PM</span></span>
                <span class="span2 scheduleSite"><span>Orchard</span></span>
                <span class="span3 scheduleClass"><span>Total Body</span>
                <i class="icon-info-sign pop" data-classtype="830197022001727052" data-classid="2437635024040757087" data-customtype=""></i>
                </span>
                <span class="span3 scheduleInstruc"><span>Jian Hong Teng</span></span>
                <span class="span2 classlength"><span>50 min</span></span>
            </a>
        </div>
    </div>
</div>
"""
