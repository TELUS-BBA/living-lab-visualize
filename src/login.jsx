import React from 'react';
import Input from '@tds/core-input';
import Box from '@tds/core-box';
import Button from '@tds/core-button';
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
    this.setState({
      username: event.target.value,
    });
  }

  updatePassword(event) {
    this.setState({
      password: event.target.value,
    });
  }

  render() {
    return (
      <div>
        <FlexGrid>
          <FlexGrid.Row>
            <FlexGrid.Col lg={3}>
            </FlexGrid.Col>
            <FlexGrid.Col>
              <Box inset={8} between={3}>
                <Input
                  label="Username"
                  value={this.state.username}
                  onChange={this.updateUsername}/>
                <Input
                  type="password"
                  label="Password"
                  value={this.state.password}
                  onChange={this.updatePassword} />
                <Button onClick={() => {
                  this.props.updateCredentials(this.state.username, this.state.password)
                }}>Log In</Button>
              </Box>
            </FlexGrid.Col>
            <FlexGrid.Col lg={3}>
            </FlexGrid.Col>
          </FlexGrid.Row>
        </FlexGrid>
      </div>
    );
  }
}

export default Login;
