import React from 'react';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';
import {Jumbotron,Grid,Row,Col} from 'react-bootstrap';

function Login(props) {

  return (
  <Grid>
    <Row>
      <Col xs={12}>
        <Jumbotron>
          <h1>{APP_NAME}</h1>
          <p>歡迎使用Google帳號登入.</p>
          <p>
            <ul>
              <li>簡化報名程序</li>
              <li>變更或取消報名記錄</li>
              <li>查詢個人出團記錄</li>
              <li>查詢個人團保資訊</li>
            </ul>
          </p>
          <h3>{OAUTH_CLIENT_ID}</h3>
          <p>
            <GoogleLogin
              clientId={OAUTH_CLIENT_ID}
              buttonText="使用Google登入"
              onSuccess={props.success}
              onFailure={props.failure}
            />
          </p>
        </Jumbotron>
      </Col>
    </Row>
  </Grid>
  );

}
export default Login;
