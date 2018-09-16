begin
    load "#{Rails.root}/db/seeds/#{Rails.env}.rb"
rescue LoadError
    puts "No seeds file for #{Rails.env}"
end