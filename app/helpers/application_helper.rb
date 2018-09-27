module ApplicationHelper
  def active_link_to(text = nil, path = nil, options = nil, &block)
    given_path = block_given? && text.present? ? text : path
    active     = given_path =~ /#{request.path}/ || request.path =~ /#{given_path}/ ? 'active' : ''
    content_tag :li, class: active do
      link_to text, path, options, &block
    end
  end
end
