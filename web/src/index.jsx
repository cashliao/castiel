import React from 'react';
import ReactDOM from 'react-dom';
import img1 from './people.jpg';
import { Navbar,Nav,Glyphicon} from 'react-bootstrap';
import Home from './public/home.jsx';
import Login from './public/login.jsx';
import Thumbnail from './public/thumbnail.jsx';
import SystemManagement from './system/system-management.jsx';
import ActivityManagement from './activity/activity-management.jsx';
import SignupManagement from './signup/signup-management.jsx';
import TransportManagement from './transport/transport-management.jsx';
import InsuranceManagement from './insurance/insurance-management.jsx';
import BoardingManagement from './boarding/boarding-management.jsx';
import CheckinManagement from './checkin/checkin-management.jsx';
import VolunteerManagement from './volunteer/volunteer-management.jsx';

import axios from 'axios';

const modules = [
  {id:'system',name:'系統設定',component:'SystemManagement'},
  {id:'activity',name:'活動管理',component:'ActivityManagement'},
  {id:'signup',name:'報名管理',component:'SignupManagement'},
  {id:'transport',name:'交通安排',component:'TransportManagement'},
  {id:'insurance',name:'保險管理',component:'InsuranceManagement'},
  {id:'boarding',name:'登車管理',component:'BoardingManagement'},
  {id:'checkin',name:'報到管理',component:'CheckinManagement'},
  {id:'volunteer',name:'義工資訊',component:'VolunteerManagement'}
];

class Index extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
       logined : false,
       module:''
    };
    this.loginSuccess = this.loginSuccess.bind(this);
    this.loginFailure = this.loginFailure.bind(this);
    this.run = this.run.bind(this);
  }

  loginSuccess(googleUser) {
    //var profile = googleUser.getBasicProfile();
    //var token = googleUser.getAuthResponse().id_token;
    //var name = profile.ig;
    //var email = profile.U3;
    this.setState({logined:true});
  }

  loginFailure(err) {
    alert('登入失敗,請重新登入');
  }

  run(id) {
    this.setState({module:id});
  }

  render() {
    var body = null;
    if (this.state.logined == false) {
      body = <Login success={this.loginSuccess} failure={this.loginFailure}/>;
    } else if (this.state.module == '') {
      body = <Home modules={modules} run={this.run}/>;
    } else {
      var m = modules.find((ob)=>{ return ob.id==this.state.module; });
      const TagName = m.component;
      body = <TagName run={this.run}/>;
    }

    return (
      <div>
        <Navbar>
          <Navbar.Header>
            <Navbar.Brand>
              <a href="#" onClick={(e)=>this.setModule('')}>
                <Glyphicon glyph="home" style={{margin:'4px 10px 4px 10px'}}/>
                {APP_NAME}
              </a>
            </Navbar.Brand>
          </Navbar.Header>
        </Navbar>
        <div>
          {body}
        </div>
      </div>
    )
  };
}

ReactDOM.render(<Index />, document.getElementById('index'));
