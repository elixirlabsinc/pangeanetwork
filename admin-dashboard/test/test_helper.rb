require File.expand_path('../config/environment', __dir__)
require 'rails/test_help'
require 'factory_bot'

FactoryBot.find_definitions

class ActiveSupport::TestCase
  include FactoryBot::Syntax::Methods
  include ActionView::Helpers::NumberHelper

  # Add more helper methods to be used by all tests here...
end
