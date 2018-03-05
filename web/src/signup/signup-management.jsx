import React from 'react';
import ReactDOM from 'react-dom';
import { Table,Glyphicon,Grid,Row,Col,ButtonGroup,Button } from 'react-bootstrap';

class SignupManagement extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
    };
  }

  render() {  
    var rows  = [];
    var item = {no:1,name:'Mission One',start:'2018-02-10',end:'2018-02-11',oldLimit:10,newLimit:20,status:'Actived' };
    rows.push(
      <tr>
        <td>{item.no}</td>
        <td>{item.name}</td>
        <td>{item.start}~{item.end}</td>
        <td>{item.status}</td>
        <td>
          <ButtonGroup className="pull-right">
            <Button>編輯</Button>
            <Button>資料</Button>
            <Button bsStyle="danger">封存</Button>
          </ButtonGroup>
        </td>
      </tr>
    );

    return (
      <Grid>
        <Row><h1><span style={{margin:'10px'}}>報名管理</span><small><Button>新增活動</Button></small></h1>
       </Row>
        <Row>
          <ButtonGroup className="pull-right">
          </ButtonGroup>
        </Row>
        <Row>
          <Table>
            <thead>
              <tr>
                <th>#</th>
                <th>活動名稱</th>
                <th>活動區間</th>
                <th>狀態</th>
                <th>編輯</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </Table>
        </Row>
      </Grid>
    )
  };
}
export default SignupManagement
