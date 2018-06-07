import React from 'react';
import Input from '@tds/core-input';
import Box from '@tds/core-box';
import FlexGrid from '@tds/core-flex-grid';

class Login extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      username: this.props.username,
      password: this.props.password,
    }
    this.updateUsername = this.updateUsername.bind(this);
    this.updatePassword = this.updatePassword.bind(this);
  }

  updateUsername(event) {
    this.props.updateCredentials(event.target.value, this.state.password);
    //    this.setState({
    //      username: event.target.value,
    //    });
  }

  updatePassword(event) {
    this.props.updateCredentials(this.state.username, event.target.value);
    this.setState({
      password: event.target.value,
    });
  }

  render() {
    return (
      <div>
        <Box horizontal={1} vertical={3}>
          <FlexGrid>
            <FlexGrid.Row>
              <FlexGrid.Col>
                <Input
                  label="Username"
                  value={this.props.username}
                  onChange={this.updateUsername}
                />
              </FlexGrid.Col>
              <FlexGrid.Col>
                <Input
                  type="password"
                  label="Password"
                  value={this.props.password}
                  onChange={this.updatePassword}
                />
              </FlexGrid.Col>
            </FlexGrid.Row>
          </FlexGrid>
        </Box>
      </div>
    );
  }
}

export default Login;

//                <Button onClick={() => {
//                  this.props.updateCredentials(this.state.username, this.state.password)
//                }}>Log In</Button>
