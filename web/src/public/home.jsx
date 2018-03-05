import React from 'react';
import ReactDOM from 'react-dom';
import Thumbnail from './thumbnail.jsx';
import { Grid,Row,Col,ButtonGroup,Button } from 'react-bootstrap';

function Home(props) {
  return (
    <Grid>
      <Row>
        <Col xs={12} sm={6} md={4}>
          <Thumbnail glyph="pencil" title="活動管理" desc="設定活動,人數限制,交通方式,活動統計等">
            <Button bsStyle='primary' onClick={(e)=>props.module('signup')}>執行</Button>
          </Thumbnail>
        </Col>
        <Col xs={12} sm={6} md={4}>
          <Thumbnail glyph="pencil" title="報名作業" desc="開放報名,設定人數上限及其相關作業">
            <Button bsStyle='primary' onClick={(e)=>props.module('signup')}>執行</Button>
          </Thumbnail>
        </Col>
        <Col xs={12} sm={6} md={4}>
          <Thumbnail glyph="road" title="出團作業" desc="出團名單/交通安排/新人名冊/旅平險清冊/統計資訊等">
            <Button bsStyle='primary'  onClick={(e)=>props.module('missions')}>執行</Button>
          </Thumbnail>
        </Col>
        <Col xs={12} sm={6} md={4}>
          <Thumbnail glyph="road" title="交通作業" desc="上車地點,時間,及遊覽車/交通車/徵調車安排">
            <Button bsStyle='primary'  onClick={(e)=>props.module('missions')}>執行</Button>
          </Thumbnail>
        </Col>
        <Col xs={12} sm={6} md={4}>
          <Thumbnail bsStyle='primary'  glyph="grain" title="保險作業" desc="團保記錄/單次旅平險作業等">
            <Button bsStyle='primary' onClick={(e)=>props.module('insurance')}>執行</Button>
          </Thumbnail>
        </Col>
        <Col xs={12} sm={6} md={4}>
          <Thumbnail bsStyle='primary'  glyph={'user'} title="義工名冊" desc="個人資料,專長,出團記錄查詢等">
            <Button bsStyle='primary'  onClick={(e)=>props.module('members')}>執行</Button>
          </Thumbnail>
        </Col>
        <Col xs={12} sm={6} md={4}>
          <Thumbnail glyph="cog" title="系統管理" desc="系統管理/權限設定/通知設定等">
            <Button bsStyle='primary' onClick={(e)=>props.module('system')}>執行</Button>
          </Thumbnail>
        </Col>
      </Row>
    </Grid>
  );
 }
export default Home;
